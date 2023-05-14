def get_room_users(table, room_id):
    scan_response = table.scan(
        ProjectionExpression='connection_id,user_name',
        FilterExpression="room_id = :id",
        ExpressionAttributeValues={
            ":id": room_id   
        })
    users = set(
        (item['connection_id'], item['user_name']) for item in scan_response['Items']
    )
    return users