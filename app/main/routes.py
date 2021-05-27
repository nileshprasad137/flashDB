import uuid, json
from flask import session, redirect, url_for, render_template, request, jsonify, Response
from . import main
from flask_login import current_user
from flask_socketio import disconnect
from .helper_functions import is_document_present
from .. import mongo_client, master_flash_db_client, create_required_collections


@main.route('/register-client', methods=['GET'])
def index():
    """Register Client"""
    data = request.json
    client_id = uuid.uuid4()
    response = {"client_id": str(client_id)}
    # Also store in mongo db
    client_data = { "client_id": str(client_id) }
    master_flash_db_client["clients"].insert_one(client_data)
    return jsonify(response)
    

@main.route('/create-client-project', methods=['POST'])
def create_client_project():
    """ Create client project. """
    # QUESTION: Do i need to check if that particluar clinet_id is connected to socket?
    data = request.json
    client_id = data["client_id"]
    project_name = data["project_name"]
    status = False
    message = str()
    if is_document_present("clients", {"client_id" : client_id}):
        project_data = { "project_name": project_name, "project_owner": client_id }
        if not is_document_present("projects", project_data):
            inserted_data = master_flash_db_client["projects"].insert_one(project_data)
            if inserted_data:
                status = True
                message = "Project creation successful!"
    if not status:
        message = "Project creation failed as this client_id is not present, or project already created!"

    response = {"status": status, "message": message}
    return Response(
        response=json.dumps(response),
        status=200 if status else 400,
        mimetype='application/json'
    )

@main.route('/create-client-db', methods=['POST'])
def create_client_db():
    data = request.json
    client_id = data["client_id"]
    project_name = data["project_name"]
    client_database_name = data["database_name"]
    status = False
    message = str()
    client_query = {"client_id" : client_id}
    project_query = { "project_name": project_name, "project_owner": client_id }
    if is_document_present("clients", client_query) and is_document_present("projects", project_query):
        formatted_client_database_name = client_id + "-" + client_database_name
        if formatted_client_database_name not in mongo_client.list_database_names():
            new_client_database = mongo_client[formatted_client_database_name]
            init_collections = ["init_coll"]
            create_required_collections(init_collections, formatted_client_database_name)
            clientdb_project_mapping_data = {
                "client_id": client_id,
                "project_name": project_name,
                "database_name": formatted_client_database_name,
                "subscribers": [
                    client_id
                ]
            }
            master_flash_db_client["clientdb_project_mapping"].insert_one(clientdb_project_mapping_data)
            status = True
            message = "Database creation successful!"
    if not status:
        message = "Database creation failed as client_id, project_id not found or database already in existence."
    response = {"status": status, "message": message}
    return Response(
        response=json.dumps(response),
        status=200 if status else 400,
        mimetype='application/json'
    )


@main.route('/create-client-collection', methods=['POST'])
def create_client_collection():
    data = request.json
    client_id = data["client_id"]
    project_name = data["project_name"]
    client_database_name = data["database_name"]
    formatted_client_database_name = client_id + "-" + client_database_name
    client_collection_name = data["collection_name"]
    status = False
    message = str()
    client_query = {"client_id" : client_id}
    project_query = { "project_name": project_name, "project_owner": client_id }
    client_database_query = { "project_name": project_name, "client_id": client_id, "database_name": formatted_client_database_name }
    if is_document_present("clients", client_query) and is_document_present("projects", project_query) and is_document_present("clientdb_project_mapping", client_database_query): 
        create_required_collections([client_collection_name], database_name=formatted_client_database_name)
        status = True
        message = "Collection for client created successfully!"
    if not status:
        message = "something went wrong!"
    response = {"status": status, "message": message}
    return Response(
        response=json.dumps(response),
        status=200 if status else 400,
        mimetype='application/json'
    )


@main.route('/create-client-document', methods=['POST'])
def create_client_document():
    data = request.json
    client_id = data["client_id"]
    project_name = data["project_name"]
    client_database_name = data["database_name"]
    formatted_client_database_name = client_id + "-" + client_database_name
    client_collection_name = data["collection_name"]
    # TODO document sanitisation need to be done before populating.
    client_document = data["document_data"]
    status = False
    message = str()
    client_query = {"client_id" : client_id}
    project_query = { "project_name": project_name, "project_owner": client_id }
    client_database_query = { "project_name": project_name, "client_id": client_id, "database_name": formatted_client_database_name }
    if is_document_present("clients", client_query) and is_document_present("projects", project_query) and is_document_present("clientdb_project_mapping", client_database_query): 
        if client_collection_name in mongo_client[formatted_client_database_name].list_collection_names():
            mongo_client[formatted_client_database_name][client_collection_name].insert_one(client_document)
        status = True
        message = "Document for client created successfully!"
    if not status:
        message = "something went wrong!"
    response = {"status": status, "message": message}
    return Response(
        response=json.dumps(response),
        status=200 if status else 400,
        mimetype='application/json'
    )

# TODO UPDATE DOCS API

"""
# client can create app/project
# Client can create database
# Client can create document
# clients can subscribe to app/db/table updates.
"""
