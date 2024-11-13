from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ait'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@socketio.on('message')
def handle_message(msg):
    if msg != '':  # 빈 메시지는 처리하지 않음
        print('Message: ' + msg)
        send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)