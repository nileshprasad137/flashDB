import redis
from flask import session, request
from flask_socketio import emit, join_room, leave_room, disconnect, send, rooms
from .. import socketio, master_flash_db_client, redis_client
from app.utils.helper_functions import RedisWrapper

connected_clients = []
redis_helper = RedisWrapper()

@socketio.on('connect', namespace="/test")
def connect():
    print('connection established by someone.')
    token = request.args.get('token') # /?token=uuid_dummy
    print(token)
    project_name = request.args.get('project')
    session['project'] = project_name
    clients = master_flash_db_client.clients
    results = clients.find_one({"client_id": token})
    print(results)
    if not results:
        disconnect()
    print("project_name = ", project_name)
    room = project_name
    # TODO Before joining room, check if that particular token is authorised to enter the room.
    redis_helper.sub(room=project_name)
    join_room(project_name)
    emit('joined', {
        'data': {
            "message": "Hello " + token + ". You joined " + room
        }},

    )
    # TODO should I store historic connection data at Mongo ?
    client_connection_detail = {
            'client_session': str(request.sid),
            'client_ip': str(request.access_route),
            'token': token
    }
    # print connected clients' 
    connected_clients.append(client_connection_detail)
    redis_client.hmset(token, client_connection_detail)
    # does it need "join" event????
    print(connected_clients)
    print(room)
    emit('message', {
        'data': {
            "message": token + " joined " + room
        }},
        room=room
    )
    # print(socketio)
    # print(redis_client.hgetall(token))
    # print(redis_client.exists(token))

@socketio.on('disconnect', namespace="/test")
def disconnect():
    emit('banned', {'data': "you are kicked out of socket. you wont be able to send messages now."})
    print('disconnected (catched on server side)')
    token = request.args.get('token')
    redis_client.delete(token)
    print("session['project'] ::", session['project'])
    leave_room(session['project'])
    redis_helper.un_sub()
    # remove from connected_clients
    # clients.remove(request.namespace)


@socketio.on('after', namespace="/test")
def connect():
    print('after disconnect.')

# @socketio.on('joined', namespace='/chat')
# def joined():
#     """Sent by clients when they enter a room.
#     A status message is broadcast to all people in the room."""
#     room = session.get('room')
#     join_room(room)
#     emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('message', namespace='/chat')
def message(message):
    """user sends a new message. This message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
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