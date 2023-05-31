from app.vue._blueprints import vue_bp
from flask import request, abort, render_template
from core import log, streams


@vue_bp.route('/stream-list', methods=['GET'])
@vue_bp.route('/', methods=['GET'])
def stream_list():
    return render_template("list.html", title="Stream List", streams=streams.list())


@vue_bp.route('/server-log', methods=['GET'])
def server_log():
    if not request.args:
        with open(log) as f:
            lines = f.read().splitlines()
        return render_template("log.html", title="Server Log", server_logs=lines)
    else:
        abort(404)


@vue_bp.route('/stream-list/<name>', methods=['GET'])
def stream_item(name):
    stream = streams.get(name)
    if stream:
        return render_template("stream.html", title=name, stream=stream)
    else:
        abort(404)


@vue_bp.route('/new-stream', methods=['GET'])
def new_stream():
    return render_template("new.html", title="New Stream")
