def response_success(response, code=None):
    if code is None:
        assert 200 <= response.status_code < 300, 'Received %d response: %s' % (response.status_code, response.data)
    else:
        assert code == response.status_code, 'Received %d response: %s' % (response.status_code, response.data)

def response_error(response, code=None):
    if code is None:
        assert 400 <= response.status_code < 500, 'Received %d response: %s' % (response.status_code, response.data)
    else:
        assert code == response.status_code, 'Received %d response: %s' % (response.status_code, response.data)

def compare_req_resp(req_obj, resp_obj):
    for k,v in req_obj.iteritems():
        assert k in resp_obj.keys(), 'Key %r not in response (keys are %r)' % (k, resp_obj.keys())
        assert resp_obj[k] == v, 'Value for key %r should be %r but is %r' % (k, v, resp_obj[k])
