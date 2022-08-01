import json
import boto3
from botocore.exceptions import ClientError


def sign_in(email, password):
    # 認証開始
    try:
        aws_client = boto3.client(
            'cognito-idp'
        )

        aws_result = aws_client.admin_initiate_auth(
            UserPoolId="ap-northeast-1_MaHm14Msn",
            ClientId="674ab2m9u0r14eaebjik9da9mu",
            # AuthFlow="ADMIN_USER_PASSWORD_AUTH",
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password,
            }
        )

        # 本登録完了
        return [aws_result]

    except ClientError as e:
        # print(e.response['Error']['Code'f])
        # 認証失敗
        if e.response['Error']['Code'] == 'NotAuthorizedException':
            message =  "Login failed"
        elif e.response['Error']['Code'] == 'UserNotConfirmedException':
            message =  "Not confirmed"
        else:
            message =  "Unexpected error: %s" % e
        return ['error', message]


def handler(event, context):
    json_data = json.loads(event['body'])
    result = sign_in(json_data['email'], json_data['password'])

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
            "message": "login successful",
            'AccessToken': result[0]['AuthenticationResult']['AccessToken'],
            'RefreshToken': result[0]['AuthenticationResult']['RefreshToken'],
            'IdToken': result[0]['AuthenticationResult']['IdToken']
        }

        response = {
            "statusCode": 200,
            "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
            },
            "body": json.dumps(body)
        }

    return response
