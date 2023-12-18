import json
import boto3
import csv

TABLE = 'new_repos_store'
S3BUCKET = 'opensource-personalize-traning'
S3KEY = 'item-data.csv'

def lambda_handler(event, context):
    # read data from the new_repos_store every 10 minutes
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')
    
    tableClient = dynamodb.Table(TABLE)
    response = tableClient.scan(Limit=20)
    repos = response.get('Items', [])
    
    repo_data = []
    
    existing_csv = []
    if len(repos) > 0 :
        try:
            existing_data = s3.get_object(Bucket=S3BUCKET, Key=S3KEY)
            existing_csv = list(csv.reader(existing_data['Body'].read().decode('utf-8').splitlines()))
        except s3.exceptions.NoSuchKey:
            pass  # File doesn't exist yet, no need to append
            return 0
    
    for repo in repos:
        item_id = repo.get('repo_url')
        item_id = item_id[19:]
        languages = '|'.join(repo.get('language', [])[:2]).lower().replace(" ", "")
        topics = '|'.join(repo.get('topics', [])[:2]).lower().replace(" ", "")
        existing_csv.append([item_id, languages, topics])
    
    s3.put_object(
        Bucket=S3BUCKET,
        Key=S3KEY,
        Body=bytes('\n'.join([','.join(map(str, row)) for row in existing_csv]), 'utf-8')
    )
    
    # Delete the values from new_repos after processing
    for repo in repos:
        tablClient.delete_item(
            Key={
                'repo_url': repo['repo_url']
            }
        )
    # Delete the data and update the data on s3 csv file 
    
    
    return 0
