import json

from auxiliary_functions.get_room_users import get_room_users
from auxiliary_functions.handle_ws_message import handle_ws_message


def update_connected_users(table, room_id, apig_management_client, recipients = "All"):
    room_users = get_room_users(table, room_id)
    message = json.dumps({"connected_users":{
        "usernames": [user[1] for user in room_users]
    }})

    if recipients == "All":
        recipients = [user[0] for user in room_users]

    handle_ws_message(table, recipients, message, apig_management_client)
    return 200