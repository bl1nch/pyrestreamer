import psutil
import GPUtil


def start_monitoring(socketio):
    thread = socketio.start_background_task(monitoring, socketio)
    return thread


def monitoring(socketio):
    while True:
        gpu_load, mem_load = 0, 0
        for gpu in GPUtil.getGPUs():
            gpu_load += round(gpu.load * 100, 1)
            mem_load += round(gpu.memoryUtil * 100, 1)
        data = {'cpu': psutil.cpu_percent(2), 'ram': psutil.virtual_memory().percent, 'gpu': gpu_load, 'mem': mem_load}
        socketio.emit('monitoring', {'data': data})
