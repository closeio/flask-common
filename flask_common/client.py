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
            resp.json = json.loads(resp.data)
        except ValueError:
            pass
        return resp

def local_request(view, args=None, user=None, view_args=None, api_key=None):
    if not view_args:
        view_args = {}
    ctx = current_app.test_request_context()
    ctx.request.args = args
    ctx.user = user
    ctx.g.api_key = api_key
    ctx.push()
    data = view.dispatch_request(**view_args).data
    json_data = json.loads(data)
    ctx.pop()
    return json_data
