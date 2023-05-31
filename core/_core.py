from config import create_app, setup_logging, start_monitoring
from pysondb import getDb
from extensions.streaming import StreamPool


app, socketio = create_app()
log = setup_logging(socketio=socketio)
monitor = start_monitoring(socketio=socketio)
db = getDb(filename="db.json", log=app.debug)
streams = StreamPool(quiet=app.debug)
