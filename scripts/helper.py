from flask import request, make_response, current_app
from datetime import timedelta
from functools import update_wrapper
import requests


class SlackApi:

    def __init__(self,
                 webhook_url=''):
        self.webhook_url = webhook_url

    def post_message(self, text="flask file"):
        headers = {'Content-type': 'application/json'}

        data = f'{{"text": "{text}"}}'

        return requests.post(self.webhook_url, data=data.encode('utf-8'), headers=headers)


def cross_domain_cors(origin=None, methods=None, headers=None, max_age=21600,
                      attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """

        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator
