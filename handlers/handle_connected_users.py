from botocore.exceptions import ClientError
from auxiliary_functions.update_connected_users import update_connected_users


def handle_connected_users(table, event, connection_id, apig_management_client):
    status_code = 200

    try:
        item_response = table.get_item(Key={'connection_id': connection_id})
        room_id = item_response["Item"]["room_id"]

        update_connected_users(
            table, room_id, apig_management_client, recipients=[connection_id]
        )

    except ClientError:
        status_code=503

    return status_code