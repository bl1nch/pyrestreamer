from core import app, socketio, db, streams, host, port, ssl
from extensions.streaming import Stream
from app.api import api_bp
from app.vue import vue_bp
import logging


if __name__ == '__main__':
    app.register_blueprint(api_bp)
    app.register_blueprint(vue_bp)
    data = db.getAll()

    for element in data:
        element.pop("id")
        streams.add(Stream(**element))

    logging.warning('App started')
    streams.start()
    if ssl:
        socketio.run(app, host=host, port=port, certfile='certificate.pem', keyfile='privatekey.pem')
    else:
        socketio.run(app, host=host, port=port)
