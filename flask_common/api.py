import requests
import base64
import json
import urllib

class APIError(Exception):
    pass

class Client(object):
    def __init__(self, base_url, api_key):
        assert base_url
        self.base_url = base_url
        self.api_key = api_key

    def dispatch(self, method, endpoint, data=None):
        response = method(
            self.base_url+endpoint,
            data=data != None and json.dumps(data),
            headers={'Authorization' : 'Basic %s' % (base64.b64encode('%s:' % self.api_key), ), 'Content-Type': 'application/json'}
        )

        if response.ok:
            return json.loads(response.content)
        else:
            print response, response.content
            raise APIError()

    def get(self, endpoint, data=None):
        if data:
            endpoint += '/?'+urllib.urlencode(data)
        return self.dispatch(requests.get, endpoint)

    def post(self, endpoint, data):
        return self.dispatch(requests.post, endpoint+'/', data)

    def put(self, endpoint, data):
        return self.dispatch(requests.put, endpoint+'/', data)

