from email import message
import json
import boto3
from botocore.exceptions import ClientError

def sign_up(nickname, email, password):
    # 認証開始
    try:
        aws_client = boto3.client(
            'cognito-idp'
            # region_name='ap-northeast-1'
            # aws_access_key_id='',
            # aws_secret_access_key='',
        )

        aws_result = aws_client.sign_up(
            ClientId="674ab2m9u0r14eaebjik9da9mu",
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'nickname',
                    'Value': nickname
                }
            ]
        )

        # 仮登録完了
        return [aws_result]

    except ClientError as e:
        # 認証失敗
        if e.response['Error']['Code'] == 'UsernameExistsException':
            message =  "Email address already exists"
        else:
            message =  "Unexpected error: %s" % e
        return ['error', message]


def handler(event, context):
    json_data = json.loads(event['body'])
    # try:
    result = sign_up(json_data['nickname'], json_data['email'], json_data['password'])
    # except Exception as e:
    #     traceback.print_exc()
    #     result = ['error', e]

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
            "message": "tmp successful",
        }

        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(body)
        }

    return response
