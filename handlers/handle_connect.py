from botocore.exceptions import ClientError

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
    except ClientError:
        status_code = 505
    return status_code, room_id