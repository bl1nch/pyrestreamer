function server_monitoring() {
    const socket = io();
    socket.on('monitoring', function(msg) {
        cpu_obj = document.getElementById('cpu');
        cpu_obj.innerHTML = msg.data.cpu ? msg.data.cpu + "%" : "0%";
        ram_obj = document.getElementById('ram');
        ram_obj.innerHTML = msg.data.ram ? msg.data.ram + "%" : "0%";
        gpu_obj = document.getElementById('gpu');
        gpu_obj.innerHTML = msg.data.gpu ? msg.data.gpu + "%" : "0%";
        mem_obj = document.getElementById('mem');
        mem_obj.innerHTML = msg.data.mem ? msg.data.mem + "%" : "0%";
    });
}