# app.py: The main Python script that contains the Flask application logic.
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send
import time
import threading

app = Flask(__name__)
app.secret_key = "your_secret_key"
socketio = SocketIO(app)
codes = {}
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enter_code', methods=['POST'])
def enter_code():
    code = request.form['code']
    session['code'] = code
    if code not in codes:
        codes[code] = time.time()
        threading.Thread(target=wait_for_users, args=(code,)).start()
        return render_template('waiting.html')
    else:
        return redirect(url_for('nickname'))

def wait_for_users(code):
    time.sleep(60)
    if time.time() - codes[code] >= 60:
        codes.pop(code, None)
        rooms[code] = None

@app.route('/nickname', methods=['GET', 'POST'])
def nickname():
    if request.method == 'POST':
        nickname = request.form['nickname']
        session['nickname'] = nickname
        room = session.get('code')
        if room not in rooms:
            rooms[room] = []
        return redirect(url_for('chat'))
    return render_template('nickname.html')

@app.route('/chat')
def chat():
    nickname = session.get('nickname')
    room = session.get('code')
    if not nickname or not room:
        return redirect(url_for('index'))
    return render_template('chat.html', room=room, nickname=nickname)

@socketio.on('join')
def on_join(data):
    nickname = session.get('nickname')
    room = session.get('code')
    join_room(room)
    send(f"{nickname} has entered the room.", room=room)

@socketio.on('message')
def handle_message(data):
    nickname = session.get('nickname')
    room = session.get('code')
    message = f"{nickname}: {data}"
    send(message, room=room)

@app.route('/exit')
def exit():
    room = session.get('code')
    leave_room(room)
    if room in rooms:
        del rooms[room]
    return redirect(url_for('index'))

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)