"""
API for performing A2S queries
"""

import time

import flask
import valve.source.a2s
import werkzeug.contrib.cache

import sourceservers

# Minimum number of seconds between polls
MIN_POLL_SECONDS = 120

api = flask.Blueprint('api', __name__)
cache = werkzeug.contrib.cache.SimpleCache()


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
        port = host_split[1]
    elif len(host_split) != 1:
        # If the split isn't 1 or 2, multiple colons were given
        flask.abort(400, 'Multiple possible ports found in request')

    # Query Server
    server = valve.source.a2s.ServerQuerier((host, port))
    info_dict = dict(server.get_info())

    # Replace fields that aren't JSON serializable
    # TODO Make this more general
    info_dict['platform'] = str(info_dict['platform'])
    info_dict['server_type'] = str(info_dict['server_type'])

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
    return flask.jsonify(info_dict)
