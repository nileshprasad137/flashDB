
"""
Things to implement for client:
1. Client should have option whether it wants to subscribe to realtime-updates in db.
2. Function for client for seeing latest data.
3. client can toggle b/w offline/online. (function for toggling client state.)
4. client sends data. 
4. client should be able to add tables.
5. clients should be able to able to subscribe for updates in a table.
Additional features.
 - Multitenant
"""

import socketio

sio = socketio.Client()


@sio.on("connect", namespace="/test")
def connect():
    print('connection established')


@sio.on("joined", namespace="/test")
def joined(data):
    print('message received with ', data)
    # sio.emit('my response', {'response': 'my response'})


@sio.on("banned", namespace="/test")
def joined(data):
    print('message received with ', data)


@sio.on("message", namespace="/test")
def message(data):
    print('A message ', data)
    # sio.emit('my response', {'response': 'my response'})

@sio.event(namespace='/test')
def disconnect():
    print('disconnected from server')

# Client will connect to socket when it wants to connect to project.
sio.connect('http://localhost:5000/?token=1a8b2824-e7ed-40e1-9dcd-fc2de8bb1d90&project=test')
# sio.wait()