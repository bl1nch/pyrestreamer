import logging
import click
from datetime import datetime


class SocketIOHandler(logging.StreamHandler):
    def __init__(self, socketio):
        super().__init__()
        self.socketio = socketio

    def emit(self, record: logging.LogRecord) -> None:
        self.socketio.emit('log', {'data': self.format(record)})


class AntiColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return click.unstyle(super().format(record))


def setup_logging(socketio):
    log_file = "logs/" + datetime.now().strftime('%d-%b-%y %H-%M') + ".log"
    logger = logging.getLogger()
    log_format = '[{asctime} {levelname}] {message}'
    log_default_formatter = logging.Formatter(log_format, datefmt='%d-%b-%y %H:%M:%S', style='{')
    log_nocolor_formatter = AntiColorFormatter(log_format, datefmt='%d-%b-%y %H:%M:%S', style='{')

    handler = logging.StreamHandler()
    handler.setFormatter(log_default_formatter)
    logger.addHandler(handler)

    handler = logging.FileHandler(log_file, encoding='utf8')
    handler.setFormatter(log_nocolor_formatter)
    handler.setLevel(30)
    logger.addHandler(handler)

    handler = SocketIOHandler(socketio)
    handler.setFormatter(log_nocolor_formatter)
    handler.setLevel(30)
    logger.addHandler(handler)

    return log_file
