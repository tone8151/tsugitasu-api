import json
import boto3
from botocore.exceptions import ClientError
import uuid
import datetime

def handler(event, context):
    json_data = json.loads(event["body"])

    table = boto3.resource("dynamodb").Table("users")
    option = {
        "UpdateExpression": "set #a = :a, #b = :b, #c = :c",
        "ExpressionAttributeNames": {
            "#a": "bio",
            "#b": "nickname",
            "#c": "picture"
        },
        "ExpressionAttributeValues": {
            ":a": json_data["bio"],
            ":b": json_data["nickname"],
            ":c": json_data["picture"]
        }
    }
    table.update_item(**option)

    body = {
        "message": "successful",
    }

    response = {
        "statusCode": 200,
        "headers": {
        "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body)
    }

    return response
