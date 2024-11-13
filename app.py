from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# 라우트 설정
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

# 메시지 처리
@socketio.on('message')
def handle_message(msg):
    print(f'메시지 수신: {msg}')
    send(msg, broadcast=True)

# 서버 시작
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)