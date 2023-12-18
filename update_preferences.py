import json
import boto3

TABLE_NAME = 'user_data'

def lambda_handler(event, context):
    # TODO implement
    print(event)
    # print(get_count())
    # print(check_if_user('user_id', '1'))
    exists = check_if_user('user_email', 'test@gmail.com')
    if(exists):
        print("User exists - " , exists)
        new_pref = event['user_pref']
        # new_pref.extend(exists['preferences'])
        # new_pref = list(set(new_pref))
        print("New Preferences : ",new_pref)
        data = {
                    'user_id': exists['user_id'],
                    'user_email': event['user_email'],
                    'preferences': new_pref
        }
        update_user(data)
        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
            'body': 'Existing User Preferences updated',
        }
    else:
        print("User does not exist")
        new_id = get_count() + 1
        data = {
                    'user_id': new_id,
                    'user_email': event['user_email'],
                    'preferences': event['user_pref']
        }
        insert_data(data)
        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
            'body': 'New User Created',
        }

def update_user(data, db=None, table=TABLE_NAME):
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table(table)
    key = {'user_id': data['user_id']}
    update_expression = 'SET preferences = :value'
    expression_attribute_values = {':value': data['preferences']}
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
    
def get_count(table=TABLE_NAME):
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table(table)
    response = table.scan(Select='COUNT')
    item_count = response['Count']
    return item_count
    
def insert_data(data, db=None, table=TABLE_NAME):
    if not db:
        db = boto3.resource('dynamodb')
        _table = db.Table(table)
    if data:
        response = _table.put_item(Item=data)