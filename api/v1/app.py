#!/usr/bin/python3

'''
Web service entry point
'''

from flask import Flask, jsonify
from os import getenv

# Environment variables
HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')

#: flask: app stores instance of Flask
app = Flask(__name__)

@app.route('/api/v1/status', strict_slashes=False, methods=['GET'])
def api_status():
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    app.run(
        host=HBNB_API_HOST,
        port=HBNB_API_PORT,
        debug=True
    )
