"""
UWSGI application to run csgoservers
"""

import flask

from sourceservers import api

# Set up app and register blueprints
app = flask.Flask(__name__)
app.register_blueprint(api.api, url_prefix='/api')


# Run the app if run as a script
if __name__ == '__main__':
    app.run(debug=True)
