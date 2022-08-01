import json
import boto3
from botocore.exceptions import ClientError


def confirm_sign_up(email, confirmation_code):
    # 認証開始
    try:
        aws_client = boto3.client(
            'cognito-idp'
        )

        aws_result = aws_client.confirm_sign_up(
            ClientId="674ab2m9u0r14eaebjik9da9mu",
            Username=email,
            ConfirmationCode=confirmation_code,
        )
        
        # 本登録完了
        return [aws_result]

    except ClientError as e:
        # 認証失敗
        if e.response['Error']['Code'] == 'CodeMismatchException':
            message =  "Wrong confirmation code"
        elif e.response['Error']['Code'] == 'ExpiredCodeException':
            message =  "Code is not valid"
        else:
            message =  "Unexpected error: %s" % e
        return ['error', message]


def handler(event, context):
    json_data = json.loads(event['body'])
    result = confirm_sign_up(json_data['email'], json_data['confirmation_code'])

    if result[0] == 'error':
        body = {
            "message": result[1],
        }
        response = {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(body)
        }
    else:
        body = {
            "message": "prd successful",
        }

        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(body)
        }

    return response
