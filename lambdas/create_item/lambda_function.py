import json
import os
import uuid
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def _response(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
        },
        "body": json.dumps(body, default=str),
    }

def lambda_handler(event, context):
    try:
        if "body" not in event or event["body"] is None:
            return _response(400, {"message": "Missing request body"})

        body = json.loads(event["body"], parse_float=Decimal)

        
        name = body.get("name")
        if not name or not isinstance(name, str):
            return _response(400, {"message": "Field 'name' is required and must be a string"})

        item_id = str(uuid.uuid4())
        item = {"id": item_id, **body}

        table.put_item(Item=item)

        return _response(201, {"message": "Item created", "item": item})
    except Exception as e:
        return _response(500, {"message": "Server error", "error": str(e)})