import json
import boto3

TABLE_NAME = 'user_data'

def lambda_handler(event, context):
    print(event)
    
    exists = check_if_user('user_email', event["user_email"])
    if(exists):
        print("User exists", exists)
        if event['action'] == 'like':
            like_repo(event, exists)
        else:
            unlike_repo(event, exists)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': 'action complete ',
        }
    else:
        print("User does not exist")
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': 'User Does not exist',
        }

def like_repo(event, existing_user):
    print("User exists", existing_user)
    liked_repos = (event['repo_url'])
    if(existing_user['liked_repos'] is not None):
        liked_repos.extend(existing_user['liked_repos'])
    liked_repos = list(set(liked_repos))
    data = {
            'user_id': existing_user['user_id'],
            'user_email': event['user_email'],
            'liked_repos': liked_repos
        }
    update_user(data)

def unlike_repo(event, existing_user):
    print("User exists", existing_user)
    
    if(existing_user['liked_repos'] is not None and len(existing_user['liked_repos']) != 0):
        liked_repos = existing_user['liked_repos']
        liked_repos.remove(event['repo_url'][0])
        liked_repos = list(set(liked_repos))
        data = {
                'user_id': existing_user['user_id'],
                'user_email': event['user_email'],
                'liked_repos': liked_repos
            }
        update_user(data)
    else:
        print('No Liked repos')
    
def update_user(data, db=None, table=TABLE_NAME):
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table(table)
    key = {'user_id': data['user_id']}
    update_expression = 'SET liked_repos = :value'
    expression_attribute_values = {':value': data['liked_repos']}
    response = table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'  # Optional: You can choose 'ALL_OLD' or 'NONE' as well
    )
    updated_item = response.get('Attributes', {})
    print(updated_item)

def check_if_user(key, value, table=TABLE_NAME):
    search_attribute_name = key
    search_attribute_value = value
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table(table)
    response = table.scan(
        FilterExpression=f'{search_attribute_name} = :value',
        ExpressionAttributeValues={':value': search_attribute_value}
    )
    items = response.get('Items', [])
    if(len(items) != 0):
        return items[0]
    else:
        return False
