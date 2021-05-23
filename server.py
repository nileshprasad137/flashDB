# https://python-socketio.readthedocs.io/en/latest/server.html

import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

"""
Things to implement:
1. Client should have option whether it wants to subscribe to realtime-updates in db.
2. Function for client for seeing latest data.
3. client can toggle b/w offline/online. (function for toggling client state.)
4. client sends data. 
5. client can sync data when it has lost some realtime updates.
"""