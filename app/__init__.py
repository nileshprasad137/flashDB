import pymongo
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager


socketio = SocketIO()
# Establish db connection.
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db_client = mongo_client["flashdb"] 
print(mongo_client.list_database_names())
collection_list = db_client.list_collection_names()
# Add collection for clients if it doesn't exist
collection_list = db_client.list_collection_names()
if "clients" in collection_list:
    print("The collection exists.")
else:
    client_collection = db_client["clients"]
    test_data = { "client_id": "TEST" }
    inserted_data = client_collection.insert_one(test_data)
# TODO Handle db connection failures.

def create_app(debug=True):
    """Create the app."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
