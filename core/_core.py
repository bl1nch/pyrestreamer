from config import create_app, setup_logging, start_monitoring
from pysondb import getDb
from extensions.streaming import StreamPool
from apscheduler.schedulers.gevent import GeventScheduler


host, port = '0.0.0.0', 5050
app, socketio = create_app()
log = setup_logging(socketio=socketio)
monitor = start_monitoring(socketio=socketio)
db = getDb(filename="db.json", log=app.debug)
scheduler = GeventScheduler()
streams = StreamPool(quiet=not app.debug, scheduler=scheduler)
scheduler.start()
