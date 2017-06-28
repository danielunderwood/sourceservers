"""
API for performing A2S queries
"""

import json
import time

import flask
import valve.source.a2s
import werkzeug.contrib.cache

import sourceservers

# Minimum number of seconds between polls
MIN_POLL_SECONDS = 120

api = flask.Blueprint('api', __name__)
cache = werkzeug.contrib.cache.SimpleCache()


def try_abort(func, abort_code, abort_message='', *args, **kwargs):
    """
    Tries func with kwargs and aborts with abort code and message if an
    exception is encountered

    @param  func:  Function to try
    @param  abort_code:  Flask abort code to abort with
    @param  abort_message: Message to abort with
    @param  *args:  args to pass to func
    @param  **kwargs:  kwargs to pass to func
    """
    try:
        return func(*args, **kwargs)
    except:
        flask.abort(abort_code, abort_message)


def get_server_info(host):
    """
    Gets server info for the specified host

    @param  host:  Hostname of server. host:port string if a port different
                   than the default of 27015
    @return  Dictionary of server information
    """
    # Get port number from host string if provided
    port = 27015
    host_split = host.split(':')
    if len(host_split) == 2:
        host = host_split[0]
        port = try_abort(int, 400, 'Port not integer', host_split[1])
        print(port)
    elif len(host_split) != 1:
        # If the split isn't 1 or 2, multiple colons were given
        flask.abort(400, 'Multiple possible ports found in request')

    # Query Server
    server = valve.source.a2s.ServerQuerier((host, port))
    info = try_abort(server.get_info, 404, 'Server not found')
    players = server.get_players()
    players_list = [unicode(player['name']).encode('utf-8').decode('unicode-escape')
                    for player in players['players'] if player['name']]
    info_dict = dict(info)
    info_dict.update({'players': players_list})

    return info_dict


def query_or_cache(host):
    """
    Returns the server info from the cache if it's available and recent or polls
    the server for info


    @param  host:  Hostname of server. host:port string if a port different
                   than the default of 27015
    @return  Dictionary of server information
    """
    cached_info = cache.get(host)

    if cached_info is None:
        # Get server info and add to cache if it didn't exist
        info = get_server_info(host)
        cache.set(host, info, timeout=MIN_POLL_SECONDS)
        return get_server_info(host)
    else:
        return cached_info


@api.route('/')
def api_info():
    """
    Provides API info
    """
    info_dict = {
        'version': sourceservers.__version__
    }
    return flask.jsonify(info_dict)


@api.route('/servers/<host>')
def server_info(host):
    """
    Gets the server's info

    @param  host:  Hostname of server. host:port string if a port different
                   than the default of 27015
    """
    info_dict = query_or_cache(host)

    # Replace any fields that are JSON serializable by their string
    # representations
    info_str = json.dumps(info_dict, default=str)
    info_dict = json.loads(info_str)

    return flask.jsonify(info_dict)
