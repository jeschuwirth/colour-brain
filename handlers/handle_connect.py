import json

from botocore.exceptions import ClientError
from auxiliary_functions.handle_ws_message import handle_ws_message
from auxiliary_functions.get_all_recipients import get_all_recipients

def handle_connect(table, event, connection_id, apig_management_client):
    status_code = 200

    user_name = event.get('queryStringParameters', {'name': 'guest'}).get('name')
    room_id = event.get('queryStringParameters', {'room': "aaaa"}).get("room")
    
    try:
        table.put_item(Item={
            'connection_id': connection_id,
            'room_id': room_id,
            'user_name': user_name,
        })
        message = json.dumps({"new_connection":{"id": connection_id, "user_name": user_name}})
        recipients = get_all_recipients(table, room_id)
        handle_ws_message(table, recipients, message, apig_management_client)
    except ClientError:
        status_code = 503
    return status_code