import redis
from flask import session, request
from flask_socketio import emit, join_room, leave_room, disconnect
from .. import socketio, db_client, redis_client

connected_clients = []


@socketio.on('connect', namespace="/test")
def connect():
    print('connection established by someone.')
    token = request.args.get('token') # /?token=uuid_dummy
    print(token)
    clients = db_client.clients
    results = clients.find_one({"client_id": token})
    print(results)
    if not results:
        disconnect()
    emit('joined', {
        'data': {
            "message": "Hello " + token
        }}
    )
    # should I store historing connection data at Mongo ?
    client_connection_detail = {
            'client_session': str(request.sid),
            'client_ip': str(request.access_route),
            'token': token
    }
    connected_clients.append(client_connection_detail)
    redis_client.hmset(token, client_connection_detail)
    # print(connected_clients)
    # print(redis_client.hgetall(token))
    # print(redis_client.exists(token))

@socketio.on('disconnect', namespace="/test")
def connect():
    emit('banned', {'data': "you are kicked out of socket. you wont be able to send messages now."})
    print('disconnected (catched on server side)')
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


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)