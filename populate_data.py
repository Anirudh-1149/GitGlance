import requests
import json
import boto3
from botocore.exceptions import ClientError

# === variables ===
GH_TOKEN = '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'
URL = 'https://api.github.com/search/issues'
HEADERS = {
    'Authorization': f'Bearer {GH_TOKEN}'
}
TABLE_NAME = 'repo_store'
sqs_client = boto3.client('sqs')


def lambda_handler(event, context):
    print('event: ', event)
    page = 1
    sqs_res = get_from_sqs()
    if 'Messages' in sqs_res:
        print(sqs_res['Messages'][0]['Body'])
        page = int(sqs_res['Messages'][0]['Body'])
    # page = event.get('page', 1)
    print(page)
    
    PARAMS = {
        'q': 'state:open',
        'per_page': 200,
        'page': page
    }
    
    response = requests.get(url=URL, params=PARAMS, headers=HEADERS)
    issues_repos = response.json()
    
    issues_list = []
    if response.status_code == 200:

        for repo in issues_repos['items']:
            api_repo_url = repo['repository_url']

            repo_info_response = requests.get(api_repo_url, headers=HEADERS)
            
            if repo_info_response.status_code == 200:
                repo_info_data = repo_info_response.json()
                
                
                _repo_url = '/'.join(repo['html_url'].split('/')[:-2])
                _repo_title = repo['title']
                
                # _repo_language = repo_info_data.get('language', '')
                languages_response = requests.get(api_repo_url + "/languages", headers=HEADERS)
                if languages_response.status_code == 200:
                    languages_data = languages_response.json()
                    languages = list(languages_data.keys())
                else:
                    print(languages_response)
                    languages = []
                _repo_language = languages
                
                _repo_topics = repo_info_data.get('topics', [])
                _repo_forks_count = repo_info_data.get('forks_count', 0)
                _repo_stargazers_count = repo_info_data.get('stargazers_count', 0)
                _repo_open_issues_count = repo_info_data.get('open_issues_count', 0)
                
                issue_info = {
                    'repo_url': _repo_url,
                    'title': _repo_title,
                    'language': _repo_language,
                    'topics': _repo_topics,
                    'forks_count': _repo_forks_count,
                    'stargazers_count': _repo_stargazers_count,
                    'open_issues_count': _repo_open_issues_count,
                }

                issues_list.append(issue_info)
                insert_data(issue_info)
            else:
                print(repo_info_data)
                print(f"ERROR: Repository Info --> {repo_info_response.status_code}")

        next_page = page + 1
        updated_event = {'page': next_page}
        #queue
        send_to_sqs(next_page)
        print("Inserted successfully")
        return updated_event

    else:
        print(f"Error: {response.status_code} :: Text: {response.text}")

def insert_data(data, db=None, table=TABLE_NAME):
    if not db:
        db = boto3.resource('dynamodb')
        _table = db.Table(table)
    if data:
        response = _table.put_item(Item=data)


def send_to_sqs(page_number):
    queue_url = 'https://sqs.us-east-1.amazonaws.com/270687290849/pageCount'
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(page_number)
    )
    print(f"Message sent to SQS: {response['MessageId']}", page_number)

def get_from_sqs():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/270687290849/pageCount'
    response = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0 # Adjust the batch size as needed
    )
    print("SQS MSG", response)
    if 'Messages' in response:
        sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=response['Messages'][0]['ReceiptHandle']
            )
        print("fifoed")
    return response