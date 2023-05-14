#Import handlers

from handlers.handle_message import handle_message
from handlers.handle_connected_users import handle_connected_users

#Add routes and handlers to the dict {"route_key": handler_function}
route_dic = {
    "sendmessage": handle_message,
    "connectedusers": handle_connected_users
}

def routes(route_key, table, event, connection_id, apig_management_client):
    action = route_dic[route_key]
    return action(table, event, connection_id, apig_management_client)
