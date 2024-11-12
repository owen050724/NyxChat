// chat.js: JavaScript file for managing chat functionality, like sending messages and interacting with the WebSocket.
const socket = io();

window.onload = () => {
    const room = document.querySelector('meta[name="room"]').content;
    socket.emit('join', { room });

    document.getElementById('send').onclick = () => {
        const message = document.getElementById('message').value;
        socket.send(message);
        document.getElementById('message').value = '';
    };

    document.getElementById('exit').onclick = () => {
        window.location.href = '/exit';
    };
};

socket.on('message', (msg) => {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.textContent = msg;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
});
