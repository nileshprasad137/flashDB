import uuid, json
from flask import session, redirect, url_for, render_template, request, jsonify, Response
from . import main
from flask_login import current_user
from flask_socketio import disconnect
from .helper_functions import is_document_present

@main.route('/register-client', methods=['GET'])
def index():
    """Register Client"""
    data = request.json
    client_id = uuid.uuid4()
    response = {"client_id": str(client_id)}
    # Also store in mongo db
    client_data = { "client_id": str(client_id) }
    db_client["clients"].insert_one(client_data)
    return jsonify(response)
    

@main.route('/create-client-project', methods=['POST'])
def add():
    """ Create client project. """
    data = request.json
    client_id = data["client_id"]
    project_name = data["project_name"]
    status = False
    message = str()
    if is_document_present("clients", {"client_id" : client_id}):
        client_data = { "project_name": project_name, "project_owner": client_id }
        inserted_data = db_client["projects"].insert_one(client_data)
        if inserted_data:
            status = True
            message = "Project creation successful!"
    else:
        message = "Project creation failed as this client_id is not present!"

    response = {"status": status, "message": message}
    return Response(
        response=json.dumps(response),
        status=200 if status else 400,
        mimetype='application/json'
    )

"""
# client can create app
# Client can create database
# Client can create document
# clients can subscribe to app/db/table updates.
"""
