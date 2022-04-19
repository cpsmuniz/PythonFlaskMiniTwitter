from flask import Response
import json


# Method builds a response suited for Flask with json.dumps #
def build_flask_response(status_code, body):
    response = Response(response=json.dumps(body, sort_keys=True, default=str), status=status_code, content_type='application/json')
    return response
