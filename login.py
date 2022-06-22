import json
import boto3
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

def sign_in(email, password):
    # 認証開始
    try:
        aws_client = boto3.client(
            'cognito-idp'
            # region_name='ap-northeast-1'
            # aws_access_key_id='',
            # aws_secret_access_key='',
        )

        aws_result = aws_client.admin_initiate_auth(
            UserPoolId="ap-northeast-1_ZjLlvynDn",
            ClientId="4nrc7i4dgeurnnp0ollgq28an1",
            # AuthFlow="ADMIN_USER_PASSWORD_AUTH",
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password,
            }
        )

        # 本登録完了
        return aws_result

    except:
        # 認証失敗
        return aws_result


def handler(event, context):
    json_data = json.loads(event['body'])
    result = sign_in(json_data['email'], json_data['password'])

    print("result: ", result)

    response = {
        "message": "login successful",
        'AccessToken': result['AuthenticationResult']['AccessToken'],
        'RefreshToken': result['AuthenticationResult']['RefreshToken'],
        'IdToken': result['AuthenticationResult']['IdToken']
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
