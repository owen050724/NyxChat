const socket = io();

window.onload = () => {
    const room = document.querySelector('meta[name="room"]').content;
    socket.emit('join', { room });

    document.getElementById('send').onclick = () => {
        sendMessage();
    };

    document.getElementById('message').addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });

    document.getElementById('exit').onclick = () => {
        window.location.href = '/exit';
    };
};

function sendMessage() {
    const message = document.getElementById('message').value;
    if (message.trim() !== '') {
        socket.send(message);
        document.getElementById('message').value = '';
    }
}

socket.on('message', (msg) => {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.textContent = msg;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
});