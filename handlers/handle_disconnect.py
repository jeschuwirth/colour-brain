from botocore.exceptions import ClientError

def handle_disconnect(table, event, connection_id, apig_management_client):

    status_code = 200
    room_id = 'a'
    try:
        item_response = table.get_item(Key={'connection_id': connection_id})
        room_id = item_response["Item"]["room_id"]

        table.delete_item(Key={'connection_id': connection_id})

    except ClientError:
        status_code = 503

    return status_code, room_id
