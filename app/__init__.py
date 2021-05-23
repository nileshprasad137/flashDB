import pymongo
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager


socketio = SocketIO()


def create_app(debug=True):
    """Create the app."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    # Establish db connection.
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db_client = mongo_client["flashdb"] 
    print(mongo_client.list_database_names())
    # done.
    # TODO Handle db connection failures.

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
