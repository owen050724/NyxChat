document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    document.getElementById('send-button').onclick = () => {
        let message = document.getElementById('message-input').value;
        socket.send(message);
        document.getElementById('message-input').value = '';
    };

    socket.on('message', (msg) => {
        let messages = document.getElementById('messages');
        let li = document.createElement('li');
        li.innerHTML = msg;
        messages.appendChild(li);
        messages.scrollTop = messages.scrollHeight;
    });
});