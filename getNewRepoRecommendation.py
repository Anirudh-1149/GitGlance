import json
import boto3

personalizeClient = boto3.client('personalize-runtime')
dynamodbClient = boto3.resource('dynamodb')
primaryKey = 'repo_url'
tableName = 'repo_store'

def lambda_handler(event, context):
    RepoIds = []
    recommendedRepos = []
    new_repos = ["xdy/xdy-pf2e-workbench","terraform-ibm-modules/mock-module","Jekas213/online-store","Ale6100/Proyecto-Polo-IT", "scarvalhojr/aoc-cli", "Rafmn/GB_Paradigms"]
    # user = event["queryStringParameters"]["userid"]
    user = "5"
    personalizeRecommendations = personalizeClient.get_personalized_ranking(
        campaignArn='arn:aws:personalize:us-east-1:270687290849:campaign/rankingCampaign',
        inputList = [{'itemId': item_id} for item_id in recommendedRepos],
        userId=user
    )
    
    print(personalizeRecommendations)
    repoStoreTable = dynamodbClient.Table(tableName)
    
    for item in personalizeRecommendations['itemList']:
        RepoIds.append(item['itemId'])
    
    for id in RepoIds : 
        repo_url = 'https://github.com/'+id
        tableResponse = repoStoreTable.get_item(Key={primaryKey: repo_url})
        if 'Item' in tableResponse:
            item = tableResponse['Item']
            item['forks_count'] = int(item['forks_count']),
            item['open_issues_count'] = int(item['open_issues_count'])
            item['stargazers_count'] = int(item['stargazers_count'])
            recommendedRepos.append(item), 
        else:
            print("No Table with Id : ", id)
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(recommendedRepos)
    }
