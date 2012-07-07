def response_success(response, code=200):
    if 200 <= code < 300:
        assert 200 <= response.status_code < 300
    else:
        assert code == response.status_code

def response_error(response, code=400):
    if 400 <= code < 500:
        assert 400 <= response.status_code < 500
    else:
        assert code == response.status_code

