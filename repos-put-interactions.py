import boto3
import json
import base64
from datetime import datetime
import random
import string

print('Loading function')

personalize = boto3.client('personalize-events')
kinesis_client = boto3.client('kinesis')
stream_name = 'my-stream'
trackingId = 'a4f22b4e-d4de-4b07-9834-5b431a54ee09'

def generate_session_id():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(12))
    return code

def push_event_to_Personalize(event, user_id):
    response = personalize.put_events(
        trackingId = trackingId,
        userId = user_id,
        sessionId =  generate_session_id(),
        eventList = event
    )
    print(response)
    
def lambda_handler(event, context):
    print(event)
    records = event['Records']
    record = records[-1]
    interactionBase64 = record['kinesis']['data']
    interaction = json.loads(base64.b64decode(interactionBase64).decode('utf8'))

    personalize_put_event_data = {
        'eventType': interaction["EVENT_TYPE"],
        'itemId': interaction["ITEM_ID"][19:],
        'sentAt': interaction["TIMESTAMP"]
    }
    
    push_event_to_Personalize([personalize_put_event_data], interaction['USER_ID']) 