const socket = io();

function joinWaiting(code) {
    socket.emit('join_waiting', { code });

    let timer = 60;
    const timerElement = document.getElementById('timer');
    const countdown = setInterval(() => {
        timer--;
        timerElement.textContent = timer;
        if (timer <= 0) {
            clearInterval(countdown);
            alert('No participants');
            window.location.href = '/';
        }
    }, 1000);

    socket.on('matched', (data) => {
        clearInterval(countdown);
        const nickname = prompt('Enter your nickname:', data.nickname);
        window.location.href = `/chat/${code}/${nickname}`;
    });

    socket.on('timeout', () => {
        clearInterval(countdown);
        alert('No participants');
        window.location.href = '/';
    });
}

function setupChat(room, nickname) {
    socket.emit('nickname_set', { room, nickname });

    socket.on('chat_message', (data) => {
        const chatWindow = document.getElementById('chat-window');
        const messageElement = document.createElement('div');
        messageElement.textContent = data.message;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    });
}

function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    if (message.trim() !== '') {
        socket.emit('send_message', { room, message, nickname });
        messageInput.value = '';
    }
}

function exitChat() {
    socket.emit('exit_chat', { room });
    alert('The chat has ended.');
    window.location.href = '/';
}