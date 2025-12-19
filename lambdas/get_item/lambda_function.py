import json
import os
import boto3

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
        # For HTTP API, path params appear like this:
        path_params = event.get("pathParameters") or {}
        item_id = path_params.get("id")

        if not item_id:
            return _response(400, {"message": "Missing path parameter 'id'"})

        resp = table.get_item(Key={"id": item_id})
        item = resp.get("Item")

        if not item:
            return _response(404, {"message": "Item not found"})

        return _response(200, {"item": item})
    except Exception as e:
        return _response(500, {"message": "Server error", "error": str(e)})
