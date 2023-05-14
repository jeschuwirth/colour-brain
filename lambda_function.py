import os, boto3

from handlers.routes import routes
from handlers.handle_connect import handle_connect
from handlers.handle_disconnect import handle_disconnect
from auxiliary_functions.update_connected_users import update_connected_users


dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    route_key = event.get('requestContext', {}).get('routeKey')
    connection_id = event.get('requestContext', {}).get('connectionId')
    domain = event.get('requestContext', {}).get('domainName')
    stage = event.get('requestContext', {}).get('stage')

    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)

    response = {'statusCode': 200}
    
    if table_name is None or route_key is None or connection_id is None:
        return {'statusCode': 400}
    
    if domain is None or stage is None:
        return {'statusCode': 400}

    apig_management_client = boto3.client(
        'apigatewaymanagementapi', 
        endpoint_url=f'https://{domain}/{stage}'
    )

    if route_key == '$connect':
        response['statusCode'], room_id = handle_connect(table, event, connection_id, apig_management_client)
        update_connected_users(table, room_id, apig_management_client)
    
    elif route_key == '$disconnect':
        response['statusCode'], room_id = handle_disconnect(table, event, connection_id, apig_management_client)
        update_connected_users(table, room_id, apig_management_client)

    else:
        response['statusCode'] = routes(route_key, table, event, connection_id, apig_management_client)

    return response
