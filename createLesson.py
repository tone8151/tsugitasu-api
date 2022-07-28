import json
import boto3
from botocore.exceptions import ClientError
import uuid
import datetime

def handler(event, context):
    # dynamodb_client = boto3.client(
    #     "dynamodb"
    # )
    json_data = json.loads(event["body"])

    table = boto3.resource("dynamodb").Table("lessons")

    # dt_now = datetime.datetime.now()
    t_delta = datetime.timedelta(hours=9)  # 9時間
    JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差の「JST」タイムゾーン
    dt_now = datetime.datetime.now(JST)  # タイムゾーン付きでローカルな日付と時刻を取得

    # table.put_item(Item={"lesson_id": str(uuid.uuid4()), "created_at": dt_now.strftime("%Y/%m/%d/%H:%M"), "created_by": json_data["created_by"], "icon": {"color":{"S":json_data["icon"]["color"]}, "file_name":{"S":json_data["icon"]["file_name"]}}, "materials": json_data["materials"], "outline": json_data["outline"], "Public": json_data["Public"], "tags": json_data["tags"]})
    table.put_item(Item = 
        {   
            "lesson_id": str(uuid.uuid4()),
            "lesson_name": json_data["lesson_name"], 
            "created_at": dt_now.strftime("%Y/%m/%d/%H:%M"), 
            "created_by": json_data["created_by"], 
            "icon": {"color": json_data["icon"]["color"], "file_name": json_data["icon"]["file_name"]}, 
            "materials": json_data["materials"], 
            "outline": json_data["outline"], 
            "Public": json_data["Public"], 
            "tags": json_data["tags"]
        })
    # result = confirm_sign_up(json_data["email"], json_data["confirmation_code"])

    # if result[0] == "error"1:
    #     body = {
    #         "message": result[1],
    #     }
    #     response = {
    #         "statusCode": 400,
    #         "headers": {
    #             "Access-Control-Allow-Origin": "*"
    #         },
    #         "body": json.dumps(body)
    #     }
    # else:
    body = {
        "message": "made",
    }

    response = {
        "statusCode": 200,
        "headers": {
        "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body)
    }

    return response
