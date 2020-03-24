#!/usr/bin/env python3

from flask import Flask, jsonify, request, Response
from flask_httpauth import HTTPBasicAuth
import argparse
import logging
from logging.handlers import RotatingFileHandler
import garage


port = 6001
app = Flask(__name__)
auth = HTTPBasicAuth()


@app.route('/', methods=['POST'])
@auth.login_required
def post():
    json_data = request.get_json(force=True)
    app.logger.debug(f'webhook request {json_data}')
    if 'queryResult' in json_data \
            and 'parameters' in json_data['queryResult'] \
            and 'device-type' in json_data['queryResult']['parameters'] \
            and 'service-type' in json_data['queryResult']['parameters']:
        dev_type = json_data['queryResult']['parameters']['device-type']
        ser_type = json_data['queryResult']['parameters']['service-type']

        if dev_type == 'garage door' and ser_type in ('open', 'close'):
            garage.open_close(ser_type)
            return {'fulfillmentText': 'Fulfilling your request, master!',
                    'payload': {'google': {'expectUserResponse': 'false'}}}

    app.logger.debug(f'no matching handlers for request')
    return jsonify({'fulfillmentText': 'Please say it again.'})


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return app.config['username'] == username and app.config['password'] == password


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', action='store', type=str,
                        required=True, help='HTTP basic auth username')
    parser.add_argument('-p', '--password', action='store', type=str,
                        required=True, help='HTTP basic auth password')
    parser.add_argument('-l', '--log-file-path', action='store', type=str, help='File for logs')
    return parser.parse_args()


def setup_logger(log_file_path):
    if log_file_path:
        handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=1)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    app.logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    args = parse_args()
    app.config['username'] = args.username
    app.config['password'] = args.password

    setup_logger(args.log_file_path)

    app.run(host="0.0.0.0", port=6001)
