import json
import os
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
        resp = table.scan()
        items = resp.get("Items", [])
        return _response(200, {"items": items})
    except Exception as e:
        return _response(500, {"message": "Server error", "error": str(e)})

