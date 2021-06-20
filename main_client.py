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

import socketio, json

sio = socketio.Client()


@sio.on("connect", namespace="/test")
def connect():
    print('connection established')


@sio.on("joined", namespace="/test")
def joined(data):
    print('Joining message:: ', data)


@sio.on("broadcast", namespace="/test")
def joined(data):
    print("Mesaage in room :: ", data)


@sio.on("banned", namespace="/test")
def joined(data):
    print('You were removed from room with this message:: ', data)


@sio.on("message", namespace="/test")
def message(data):
    print('Message in channel:: ', data)
    # sio.emit('my response', {'response': 'my response'})

@sio.event(namespace='/test')
def disconnect():
    print('disconnected from server')

# Client will connect to socket when it wants to connect to project.
sio.connect('http://localhost:5000/?token=6a6e0620-5715-4495-ac5a-e40a3407da60&project=test')
sio.emit('message', json.dumps({'response': 'Hi from main_client!!'}), namespace="/test")
# sio.wait()

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
