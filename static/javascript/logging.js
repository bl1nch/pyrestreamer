const socket = io();
socket.on('log', function(msg) {
    log_obj = document.getElementById('log');
    log_obj.innerHTML += ("<p>" + msg.data + "</p>");
    log_obj.scrollTop = log_obj.scrollHeight;
});