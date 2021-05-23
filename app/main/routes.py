import uuid, json
from flask import session, redirect, url_for, render_template, request
from . import main
from flask_login import current_user
from flask_socketio import disconnect, socketio



@main.route('/register', methods=['GET'])
def index():
    """Register Client"""
    data = request.json
    client_id = uuid.uuid4()
    client_secret = uuid.uuid4()
    response = {"client_id": str(client_id), "client_secret": str(client_secret)}
    session["name"] = str(client_id)
    # print(session['name'])
    # print(session.get('room', ''))
    # if not current_user.is_authenticated:
    #     socketio.disconnect()
    # Also store in mongo db
    return json.dumps(response)
    

@main.route('/connect', methods=['GET', 'POST'])
def connect_client():
    """Login form to enter a room."""
    # I can include tokens here for auth. After validating token/session, 
    # it can go ahead and connect with clent.
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)



@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)