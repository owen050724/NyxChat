const socket = io();

function setupChat(nickname) {
    socket.emit('join_chat', { nickname });

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
        socket.emit('send_message', { message, nickname });
        messageInput.value = '';
    }
}

function exitChat() {
    socket.emit('exit_chat', { nickname });
    alert('The chat has ended.');
    window.location.href = '/';
}