import boto3
import random

def lambda_handler(event, context):
    print(event)
    print(event['language'])
    
    # Language you want to search for (replace 'your_language' with the actual language)
    search_languages = event['language']
    res = {}
    response = []
    for key in search_languages:
        res[key] = based_on_language(key)
        response.extend(res.get(key))
        
    final_response = random.sample(response, min(10, len(response)))
    # Return a response if necessary
    if(len(final_response) != 0):
        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
            'body': 'Scan operation completed.',
            'result' : final_response
        }
    else:
        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
            'body': 'Scan operation completed. No Matching Response',
        }

def based_on_language(lang_key):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('repo_store')

    

    # Perform a scan with a filter expression
    response = table.scan(
        FilterExpression='contains((#lang), :lang)',
        ExpressionAttributeNames={
            '#lang': 'language'
        },
        ExpressionAttributeValues={
            ':lang': lang_key
        }
    )
    
    top_10_counter = 0


    # Extract the items from the response
    items = response.get('Items', [])
    result = random.sample(items, min(10, len(items)))
    print("total items recovered : " ,len(items))
    
    return result