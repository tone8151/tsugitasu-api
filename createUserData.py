import json
import boto3
from botocore.exceptions import ClientError

def handler(event, context):

    table = boto3.resource("dynamodb").Table("users")

    table.put_item(Item = 
        {   
            "user_id": event['userName'],
            "nickname": event['request']['userAttributes']['nickname'],
            "email": event['request']['userAttributes']['email'],
            "bio": "",
            "picture": "default"
        })

    # body = {
    #     "message": "successful",
    # }
    
    # response = {
    #     "statusCode": 200,
    #     "headers": {
    #     "Access-Control-Allow-Origin": "*",
    #     },
    #     "body": json.dumps(body)
    # }

    return event