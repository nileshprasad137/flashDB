import ast
from .. import mongo_client, redis_client, socketio

def is_document_present(collection, query, database="flashdb"):
    collection_connection = mongo_client[database][collection]
    results = collection_connection.find_one(query)
    print("Results of query :: ", results)
    return results is not None


class RedisWrapper():
    def __init__(self):
        print("redis client initialised")

    def on_message(self, data):
        """ Send any data to lobby(room) """
        print("server got a message")
        decoded_data = ast.literal_eval(data['data'].decode('utf-8'))
        print(decoded_data)
        socketio.emit("broadcast", decoded_data, namespace='/test', room=self.room)

    def sub(self, room=None):
        if not room:
            return
        self.room = room
        if hasattr(self, 'subscribed'):
            if self.subscribed:
                return
        self.pubsub = redis_client.pubsub()
        self.client = redis_client
        print("Subscribing to ", self.room)
        self.pubsub.subscribe(**{self.room: self.on_message})
        self.subscribed = True
        print(self.room , " thread started.")
        self.pubsub.run_in_thread(sleep_time=0.001)
    
    def un_sub(self):
        print("unsubscribed from  :: ", self.room)
        if hasattr(self, 'room'):
            self.pubsub.unsubscribe(self.room)
            self.subscribed = False
            self.room = None

    def pub(self, data):
        print("inside redi wrapper pub function")
        self.client.publish(self.room, data)

