import boto3
import json
from decimal import Decimal
import urllib.parse

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def player_stats(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'player-stats-l9'
    prefix = urllib.parse.unquote(event['pathParameters']['playerFullName'])
    
    response = dynamodb.Table(table_name).get_item(Key= {'playerName': prefix})
    print(response)
    
    if 'Item' in response:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response['Item'], cls=DecimalEncoder),
        }
    else:
        return {
            "statusCode": 404,
             "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Player not found"}),
        
        }
