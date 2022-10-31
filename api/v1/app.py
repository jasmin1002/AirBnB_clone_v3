#!/usr/bin/python3

'''
Web service entry point. Configure application
to run given hostname and port. Otherwise, it
uses default port 5000 and 0.0.0.0 host value
'''

from api.v1.views import app_views
from flask import Flask, json, make_response
from models import storage
from os import getenv

# Environment variables
HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')

#: flask: app stores instance of Flask
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# Register application blueprint
app.register_blueprint(app_views)


# 404 errorhandler view
@app.errorhandler(404)
def not_found(error):
    '''
    Page not found error page handler
    '''
    response = json.dumps({'error': 'Not found'}, indent=2)
    response = make_response(response)
    response.status_code = 404
    response.mimetype = 'application/json'
    return response


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
