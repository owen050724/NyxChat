from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import random
import string
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}
waiting_timers = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        return redirect(url_for('waiting', code=code))
    return render_template('index.html')


@app.route('/waiting/<code>')
def waiting(code):
    return render_template('waiting.html', code=code)


@app.route('/chat/<room>/<nickname>')
def chat(room, nickname):
    return render_template('chat.html', room=room, nickname=nickname)


@socketio.on('join_waiting')
def on_join_waiting(data):
    code = data['code']
    sid = request.sid
    nickname = random_nickname()

    if code in rooms:
        rooms[code].append(sid)
        if len(rooms[code]) == 2:
            emit('matched', {'nickname': nickname}, room=sid)
            emit('matched', {'nickname': random_nickname()}, room=rooms[code][0])
            # Cancel timer if a match is found before timeout
            if code in waiting_timers:
                waiting_timers[code].cancel()
    else:
        rooms[code] = [sid]
        timer = threading.Timer(60.0, timeout, args=[code, sid])
        waiting_timers[code] = timer
        timer.start()


@socketio.on('nickname_set')
def nickname_set(data):
    room = data['room']
    nickname = data['nickname']
    join_room(room)
    emit('chat_message', {'message': f'{nickname} has joined the chat.'}, room=room)


@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = data['message']
    nickname = data['nickname']
    emit('chat_message', {'message': f'{nickname}: {message}'}, room=room)


@socketio.on('exit_chat')
def exit_chat(data):
    room = data['room']
    leave_room(room)
    emit('chat_message', {'message': 'The chat has ended.'}, room=room)
    del rooms[room]
    if room in waiting_timers:
        del waiting_timers[room]


# Helper function to create a random nickname
def random_nickname():
    return 'User' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))


# Timeout function for waiting room
def timeout(code, sid):
    if code in rooms and sid in rooms[code]:
        rooms[code].remove(sid)
        socketio.emit('timeout', room=sid)
        if not rooms[code]:
            del rooms[code]
        if code in waiting_timers:
            del waiting_timers[code]


if __name__ == '__main__':
    socketio.run(app, debug=True)