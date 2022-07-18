from email import message
import json
import boto3
from botocore.exceptions import ClientError

def sign_up(user_nickname, email, password):
    # 認証開始
    try:
        aws_client = boto3.client(
            'cognito-idp'
            # region_name='ap-northeast-1'
            # aws_access_key_id='',
            # aws_secret_access_key='',
        )

        aws_result = aws_client.sign_up(
            ClientId="4nrc7i4dgeurnnp0ollgq28an1",
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'user_nickname',
                    'Value': user_nickname
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
    result = sign_up(json_data['user_nickname'], json_data['email'], json_data['password'])
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
