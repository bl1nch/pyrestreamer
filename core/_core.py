from config import create_app, setup_logging, start_monitoring
from pysondb import getDb
from extensions.streaming import StreamPool
from flask_apscheduler import APScheduler


ssl, host, port = False, '127.0.0.1', 5000
app, socketio = create_app()
log = setup_logging(socketio=socketio)
monitor = start_monitoring(socketio=socketio)
db = getDb(filename="db.json", log=app.debug)
scheduler = APScheduler()
scheduler.init_app(app)
streams = StreamPool(quiet=not app.debug,
                     address=('https://' if ssl else 'http://') + host + ':' + str(port),
                     scheduler=scheduler)
scheduler.start()
