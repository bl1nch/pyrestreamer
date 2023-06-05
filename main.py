from core import app, socketio, db, streams
from extensions.streaming import Stream
from app.api import api_bp
from app.vue import vue_bp


if __name__ == '__main__':
    app.register_blueprint(api_bp)
    app.register_blueprint(vue_bp)
    data = db.getAll()

    for element in data:
        element.pop("id")
        streams.add(Stream(**element))

    streams.start()
    socketio.run(app, host='127.0.0.1', port=5000, ssl_context=('certificate.pem', 'privatekey.pem'))
