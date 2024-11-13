from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nickname = request.form['nickname']
        return redirect(url_for('chat', nickname=nickname))
    return render_template('index.html')

@app.route('/chat/<nickname>')
def chat(nickname):
    return render_template('chat.html', nickname=nickname)

@socketio.on('join_chat')
def on_join_chat(data):
    nickname = data['nickname']
    join_room('chatroom')
    emit('chat_message', {'message': f'{nickname} has joined the chat.'}, room='chatroom')

@socketio.on('send_message')
def handle_send_message(data):
    message = data['message']
    nickname = data['nickname']
    emit('chat_message', {'message': f'{nickname}: {message}'}, room='chatroom')

@socketio.on('exit_chat')
def exit_chat(data):
    nickname = data['nickname']
    leave_room('chatroom')
    emit('chat_message', {'message': f'{nickname} has left the chat.'}, room='chatroom')

if __name__ == '__main__':
    socketio.run(app, debug=True)