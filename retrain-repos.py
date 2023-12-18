import boto3
import json
import base64
from datetime import datetime
import random
import string

personalize = boto3.client('personalize')

def create_import_data_job(dataset_group_arn, s3_data_location):
    job_name = 'your-import-job-name'
    
    response = personalize.create_dataset_import_job(
        jobName=job_name,
        datasetArn=dataset_group_arn,
        dataSource={
            'dataLocation': s3_data_location,
        },
        roleArn='arn:aws:iam::your-account-id:role/your-role-name',
    )

    import_job_arn = response['datasetImportJobArn']
    return import_job_arn

def create_solution(dataset_group_arn, recipe_arn):
    solution_name = 'SolutionNew'

    response = personalize.create_solution(
        name=solution_name,
        datasetGroupArn=dataset_group_arn,
        recipeArn=recipe_arn,
    )

    solution_arn = response['solutionArn']
    return solution_arn

def create_campaign(solution_arn, min_provisioned_tps, max_provisioned_tps):
    campaign_name = 'CampaignNew'

    response = personalize.create_campaign(
        name=campaign_name,
        solutionVersionArn=solution_arn,
        minProvisionedTPS=min_provisioned_tps,
        maxProvisionedTPS=max_provisioned_tps,
    )

    campaign_arn = response['campaignArn']
    return campaign_arn

def lambda_handler(event, context):
    # Replace these with your actual values
    dataset_group_arn = 'arn:aws:personalize:us-east-1:270687290849:dataset/GItGlance-dataset-group/ITEMS'
    s3_data_location = 's3://opensource-personalize-traning/item-data.csv'
    recipe_arn1 = 'arn:aws:personalize:::recipe/aws-user-personalization'
    recipie_arn2 = 'arn:aws:personalize:::recipe/aws-personalized-ranking'
    min_provisioned_tps = 1
    max_provisioned_tps = 10

    create_import_data_job(dataset_group_arn, s3_data_location)

    solution_arn1 = create_solution(dataset_group_arn, recipe_arn1)
    solution_arn2 = create_solution(dataset_group_arn,recipie_arn2)
    campaign_arn1 = create_campaign(solution_arn1, min_provisioned_tps, max_provisioned_tps)
    campaign_arn2 = create_campaign(solution_arn1, min_provisioned_tps, max_provisioned_tps)
    campaign_arn3 = create_campaign(solution_arn2, min_provisioned_tps, max_provisioned_tps)

    dynamodb = boto3.resource('dynamodb')
    table_name = 'MLLinks'
    table = dynamodb.Table(table_name)

    item1 = {
    'id': 'id1',
    'arn': campaign_arn1,
    } 

    item2 = {
    'id': 'id2',
    'arn': campaign_arn2,
    }    

    item3 = {
    'id': 'id3',
    'arn': campaign_arn3,
    } 

    table.put_item(Item=item1)
    table.put_item(Item=item2)
    table.put_item(Item=item3)


    return {
        'statusCode': 200,
        'body': 'Successfully created import job, solution, and campaign.'
    }