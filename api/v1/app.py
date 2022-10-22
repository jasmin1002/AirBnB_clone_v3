#!/usr/bin/python3

'''
Web service entry point
'''

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

# Environment variables
HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')

#: flask: app stores instance of Flask
app = Flask(__name__)
# Register application blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception):
    '''
    Terminate database session and transaction as soon as the
    http lifecycle ends.
    '''
    storage.close()


if __name__ == '__main__':
    host = HBNB_API_HOST or '0.0.0.0'
    port = HBNB_API_PORT or '5000'
    app.run(host=host, port=port, threaded=True)
