from flask import session, request
from flask_socketio import emit, join_room, leave_room, disconnect
from .. import socketio


@socketio.on('connect', namespace="/test")
def connect():
    print('connection established by someone.')
    session['keyo'] = request.args.get('token') # /a?session=example
    print(session['keyo'])
    if session['keyo']!=567:
        print("hello")
        disconnect()
    emit('joined', {'data': {"session_id":session['keyo']}})


@socketio.on('disconnect', namespace="/test")
def connect():
    print('disconnected (catched on server side)')

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