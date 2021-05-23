# https://python-socketio.readthedocs.io/en/latest/api.html#redismanager-class

import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000')
sio.wait()
 

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



