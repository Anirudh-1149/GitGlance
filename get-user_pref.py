import json
import boto3

TABLE_NAME = 'user_data'
def lambda_handler(event, context):
    exists = check_if_user('user_email', event["user_email"])
    if(exists):
         return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
            'body': 'User found',
             'user_data' : exists
        }
    else:
         return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
            'body': 'No User Found',
        }

def check_if_user(key, value, table=TABLE_NAME):

    search_attribute_name = key
    search_attribute_value = value
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table(table)
    response = table.scan(
        FilterExpression=f'{search_attribute_name} = :value',
        ExpressionAttributeValues={':value': search_attribute_value}
    )
    print(response)
    items = response.get('Items', [])
    print(items)
    if(len(items) != 0):
        return items[0]
    else:
        return False