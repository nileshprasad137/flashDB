import pymongo, redis
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager


def create_required_collections(required_collections):
    current_collections_in_db = master_flash_db_client.list_collection_names()
    for collection in required_collections:
        if collection not in current_collections_in_db:
            test_data = { "initialiser_data": "TEST" }
            db_collection = master_flash_db_client[collection]
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
print(redis_client.ping())
socketio = SocketIO()
# Establish db connection.
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
master_flash_db_client = mongo_client["flashdb"] 
print(mongo_client.list_database_names())
required_collections = ["clients", "projects", "test"]
create_required_collections(required_collections)