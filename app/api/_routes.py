from app.api._blueprints import api_bp
from extensions.streaming import Stream
from flask import request, abort
from werkzeug.datastructures import MultiDict
from core import streams, db


@api_bp.route('/status', methods=['GET'])
def status():
    name = request.args.get('name', default='none', type=str)
    needed_args = MultiDict([('name', name)])
    if needed_args == request.args:
        stream = streams.get(name)
        if stream:
            if stream.online():
                return {'found': True, 'online': True}, 200
            else:
                return {'found': True, 'online': False}, 200
        else:
            return {'found': False}, 200
    else:
        abort(404)


@api_bp.route('/stop', methods=['GET'])
def stop():
    name = request.args.get('name', default='none', type=str)
    needed_args = MultiDict([('name', name)])
    if needed_args == request.args:
        stream = streams.get(name)
        if stream:
            if stream.stop():
                return {'found': True, 'success': True}, 200
            else:
                return {'found': True, 'success': False}, 200
        else:
            return {'found': False}, 200
    else:
        abort(404)


@api_bp.route('/stop-all', methods=['GET'])
def stop_all():
    if not request.args:
        streams.stop()
        return {'done': True}, 200
    else:
        abort(404)


@api_bp.route('/start', methods=['GET'])
def start():
    name = request.args.get('name', default='none', type=str)
    needed_args = MultiDict([('name', name)])
    if needed_args == request.args:
        stream = streams.get(name)
        if stream:
            if stream.start():
                return {'found': True, 'success': True}, 200
            else:
                return {'found': True, 'success': False}, 200
        else:
            return {'found': False}, 200
    else:
        abort(404)


@api_bp.route('/start-all', methods=['GET'])
def start_all():
    if not request.args:
        streams.start()
        return {'done': True}, 200
    else:
        abort(404)


@api_bp.route('/restart', methods=['GET'])
def restart():
    name = request.args.get('name', default='none', type=str)
    needed_args = MultiDict([('name', name)])
    if needed_args == request.args:
        stream = streams.get(name)
        if stream:
            stream.restart()
            return {'found': True}, 200
        else:
            return {'found': False}, 200
    else:
        abort(404)


@api_bp.route('/restart-all', methods=['GET'])
def restart_all():
    if not request.args:
        streams.restart()
        return {'done': True}, 200
    else:
        abort(404)


@api_bp.route('/ping', methods=['GET'])
def ping():
    name = request.args.get('name', default='none', type=str)
    needed_args = MultiDict([('name', name)])
    if needed_args == request.args:
        stream = streams.get(name)
        if stream:
            if stream.ping():
                return {'found': True, 'ping': True}, 200
            else:
                return {'found': True, 'ping': False}, 200
        else:
            return {'found': False}, 200
    else:
        abort(404)


@api_bp.route('/info', methods=['GET'])
def info():
    name = request.args.get('name', default='none', type=str)
    needed_args = MultiDict([('name', name)])
    if needed_args == request.args:
        stream = streams.get(name)
        if stream:
            return {'found': True, 'info': stream.get_info()}, 200
        else:
            return {'found': False}, 200
    else:
        abort(404)


@api_bp.route('/list', methods=['GET'])
def stream_list():
    if not request.args:
        return streams.list(), 200
    else:
        abort(404)


@api_bp.route('/remove', methods=['GET'])
def remove():
    name = request.args.get('name', default='none', type=str)
    needed_args = MultiDict([('name', name)])
    if needed_args == request.args:
        stream = streams.get(name)
        if stream:
            if stream.online():
                return {'found': True, 'done': False}, 200
            else:
                stream.release()
                streams.remove(name)
                db_stream_id = db.getByQuery({"name": name})[0]['id']
                db.deleteById(db_stream_id)
                return {'found': True, 'done': True}, 200
        else:
            return {'found': False}, 200
    else:
        abort(404)


@api_bp.route('/add', methods=['GET'])
def add():
    def add_to_kwargs(item, key):
        if item != 'none':
            if key in to_int_keys:
                try:
                    kwargs[key] = int(item)
                except ValueError:
                    abort(404)
            elif key in to_bool_keys:
                try:
                    kwargs[key] = bool(item)
                except ValueError:
                    abort(404)
            else:
                kwargs[key] = item
    kwargs = {}
    to_int_keys = ['port', 'file_caching', 'video_rate', 'width', 'height', 'scale',
                   'audio_rate', 'audio_track', 'audio_channels', 'audio_sample_rate']
    to_bool_keys = ['loop']
    allowed_stream_types = ['transcode', 'standard']
    needed_args = [
        'name', 'resource', 'protocol', 'ip', 'port', 'stream_type', 'file_caching', 'multicast_output_interface',
        'video_rate', 'video_codec', 'width', 'height', 'scale', 'audio_rate', 'audio_codec', 'mux', 'loop',
        'audio_track', 'audio_channels', 'audio_sample_rate', 'subtitles_codec', 'subtitles_filter', 'logo_file'
    ]
    for arg in needed_args:
        add_to_kwargs(request.args.get(arg, default='none', type=str), arg)
    if all(arg in needed_args for arg in request.args):
        if all(key in kwargs for key in ("name", "resource", "protocol", "ip", "port", "stream_type")):
            if kwargs['stream_type'] in allowed_stream_types:
                if not streams.get(kwargs['name']):
                    new_stream = Stream(**kwargs)
                    streams.add(new_stream)
                    db.add(new_stream.get_db_info())
                    return {'done': True}
                else:
                    return {'done': False, 'info': 'Already exists'}
            else:
                return {'done': False, 'info': 'Unknown stream type'}
        else:
            return {'done': False, 'info': 'Not enough data'}
    else:
        abort(404)
