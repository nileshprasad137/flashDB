import redis, json
from flask import session, request
from flask_socketio import emit, join_room, leave_room, disconnect, send, rooms
from .. import socketio, master_flash_db_client, redis_client
from app.utils.helper_functions import RedisWrapper


@socketio.on('connect', namespace="/test")
def connect():
    print('connection established by someone.')
    token = request.args.get('token') # /?token=uuid_dummy
    project_name = request.args.get('project')
    session['project'] = project_name
    clients = master_flash_db_client.clients
    results = clients.find_one({"client_id": token})
    print(results)
    if not results:
        disconnect()
    print(token, " connected to room (project) = ", project_name)
    room = project_name
    # TODO Before joining room, check if that particular token is authorised to enter the room.
    redis_pub_sub_helper = RedisWrapper()
    redis_pub_sub_helper.sub(room=project_name)
    session['redis_pub_sub_helper'] = redis_pub_sub_helper
    join_room(project_name)
    emit('joined', {
        'data': {
            "message": "Hello " + token + ". You joined " + room
        }},
        room=room
    )
    # TODO should I store historic connection data at Mongo ?
    client_connection_detail = {
            'client_session': str(request.sid),
            'client_ip': str(request.access_route),
            'token': token
    }
    redis_client.hmset(token, client_connection_detail)
    # does it need "join" event????
    # emit('message', {
    #     'data': {
    #         "message": token + " joined " + room
    #     }},
    #     room=room
    # )
    session['redis_pub_sub_helper'].pub(json.dumps({"message": token + " joined " + room}))
    # print(socketio)
    # print(redis_client.hgetall(token))
    # print(redis_client.exists(token))

@socketio.on('disconnect', namespace="/test")
def disconnect():
    emit('banned', {'data': "you are kicked out of socket. you wont be able to send messages now."})
    token = request.args.get('token')
    print(token, ' disconnected (catched on server side). It left ', session['project'])
    # delete from redis cache
    redis_client.delete(token)
    leave_room(session['project'])
    session['redis_pub_sub_helper'].un_sub()
    # remove from connected_clients


@socketio.on('after', namespace="/test")
def connect():
    print('after disconnect.')


@socketio.on('message', namespace='/test')
def message(message):
    """user sends a new message. This message is sent to all people in the room."""
    room = session.get('project')
    print("Server received message in room :: ",room, ". Message is ->", message)
    session['redis_pub_sub_helper'].pub(message)


@socketio.on('left', namespace='/test')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


"""
1. Close room implementation. (see flask socketio docs)
2. Leave room implemenation.
3. 
"""