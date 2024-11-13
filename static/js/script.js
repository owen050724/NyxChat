document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    const form = document.getElementById('chat-form');
    const input = document.getElementById('message-input');
    const messages = document.getElementById('messages');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (input.value) {
            socket.send(input.value);
            input.value = '';
        }
    });

    socket.on('message', (msg) => {
        const item = document.createElement('li');
        item.textContent = msg;
        messages.appendChild(item);
        window.scrollTo(0, document.body.scrollHeight);
    });
});
