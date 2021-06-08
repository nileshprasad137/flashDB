# from gevent import monkey
# monkey.patch_all()
# from eventlet import monkey_patch as monkey_patch
# monkey_patch()
import pymongo, redis
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
# try:
#     from eventlet import monkey_patch as monkey_patch
#     monkey_patch()
#     print("mokey patch done.")
# except ImportError:
#     try:
#         from gevent.monkey import patch_all
#         patch_all()
#     except ImportError:
#         pass

def create_required_collections(required_collections, database_name="flashdb"):
    current_collections_in_db = mongo_client[database_name].list_collection_names()
    print("database_name :: ", database_name)
    for collection in required_collections:
        if collection not in current_collections_in_db:
            test_data = { "initialiser_data": "TEST" }
            db_collection = mongo_client[database_name][collection]
            inserted_data = db_collection.insert_one(test_data)
            if inserted_data is not None:
                print(f"Collection '{collection}' is created")
        else:
            print(f"Collection '{collection}' was already present")


def create_app(debug=True):
    """Create the app."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

redis_client = redis.Redis()
# redis_pubsub = redis_client.pubsub()
print(redis_client.ping())
socketio = SocketIO()
# Establish db connection.
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
print(mongo_client)
master_flash_db_client = mongo_client["flashdb"] 
print(master_flash_db_client)
print(mongo_client.list_database_names())
required_collections = ["clients", "projects", "test", "clientdb_project_mapping"]
create_required_collections(required_collections)