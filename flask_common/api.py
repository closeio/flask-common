import requests
import base64
import json
import urllib

class APIError(Exception):
    pass

class Client(object):
    def __init__(self, base_url, api_key, async=False):
        assert base_url
        self.base_url = base_url
        self.api_key = api_key
        self.async = async
        if async:
            import grequests
            self.requests = grequests
        else:
            self.requests = requests.session()

    def dispatch(self, method_name, endpoint, data=None):
        method = getattr(self.requests, method_name)

        response = method(
            self.base_url+endpoint,
            data=data != None and json.dumps(data),
            headers={'Authorization' : 'Basic %s' % (base64.b64encode('%s:' % self.api_key), ), 'Content-Type': 'application/json'}
        )

        if self.async:
            return response
        else:
            if response.ok:
                return json.loads(response.content)
            else:
                print response, response.content
                raise APIError()

    def get(self, endpoint, data=None):
        if data:
            endpoint += '/?'+urllib.urlencode(data)
        else:
            endpoint += '/'
        return self.dispatch('get', endpoint)

    def post(self, endpoint, data):
        return self.dispatch('post', endpoint+'/', data)

    def put(self, endpoint, data):
        return self.dispatch('put', endpoint+'/', data)

    # Only for async requests
    def map(self, requests):
        if self.async:
            import grequests
            return [(
                json.loads(response.content) if response.ok
                else APIError()
            ) for response in  grequests.map(requests)]
