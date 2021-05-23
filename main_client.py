
import socketio

sio = socketio.Client()


@sio.on("connect", namespace="/test")
def connect():
    print('connection established')

@sio.on("joined", namespace="/test")
def joined(data):
    print('message received with ', data)
    print(sio.namespaces)
    # time.sleep(1)
    sio.emit('my response', {'response': 'my response'})

# @sio.event
# def my_message(data):
#     print('message received with ', data)
#     # sio.emit('my response', {'response': 'my response'})

@sio.event(namespace='/test')
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000/?token=123')
# sio.wait()