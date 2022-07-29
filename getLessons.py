import json
import boto3
# from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import uuid
import datetime

def handler(event, context):
    user_id = event['pathParameters']['user_id']
    table = boto3.resource("dynamodb").Table("lessons")

    options = {
        'Select': 'ALL_ATTRIBUTES',
        # 'ProjectionExpression': 'lesson_name, icon, tags',
        'KeyConditionExpression': Key('created_by').eq(user_id),
        # 'FilterExpression': Attr('devices').contains('d0001'),
    }

    res = table.query(**options)

    body = res["Items"]

    response = {
        "statusCode": 200,
        "headers": {
        "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body)
    }

    return response
