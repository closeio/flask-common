import base64
import json
from flask import current_app
from werkzeug.datastructures import Headers
from werkzeug.test import Client as werkzeug_test_client

class Client(werkzeug_test_client):
    pass

class ApiClient(Client):
    def __init__(self, app, *args, **kwargs):
        self.api_key = kwargs.pop('api_key', None)
        return super(ApiClient, self).__init__(app, app.response_class, use_cookies=False)

    def get_headers(self, api_key):
        api_key = api_key or self.api_key
        return Headers([('Authorization','Basic %s' % (base64.b64encode('%s:' % api_key)))])

    def open(self, *args, **kwargs):
        # include api_key auth header in all api calls
        api_key = kwargs.pop('api_key', self.api_key)
        if 'json' in kwargs and 'data' not in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
        if 'headers' not in kwargs:
            kwargs['headers'] = self.get_headers(api_key)
        resp = super(ApiClient, self).open(*args, **kwargs)

        try:
            resp.json = lambda: json.loads(resp.data)
        except ValueError:
            pass
        return resp

def local_request(view, method='GET', data=None, view_args=None, user=None, api_key=None):
    if api_key is not None and user is not None:
        raise TypeError("local_request can only take an api_key or a user, not both.")

    if not view_args:
        view_args = {}

    ctx = current_app.test_request_context()
    ctx.request.environ['REQUEST_METHOD'] = method
    ctx.user = user
    if api_key is not None:
        ctx.g.api_key = api_key
    if data and method == 'GET':
        ctx.request.args = data
    elif data:
        ctx.request.data = json.dumps(data)
    ctx.push()

    try:
        resp = view.dispatch_request(**view_args)
        json_data = json.loads(resp.data)
    except Exception as e:
        ctx.pop()
        raise e
    else:
        ctx.pop()

    return resp.status_code, json_data
