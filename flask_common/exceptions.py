import json
from werkzeug.exceptions import HTTPException

class RESTException(HTTPException):
    def __init__(self, description=None, name=None, errors=None):
        """ 
        Base exception for API responses. We assume the client wishes to recieve JSON.

        Name --  HTTPish status.  'ish' because we translate things like 'Forbidden' into 'Access Denied'
        Description --  Human readable message. 
        Errors -- application specific error messages in the form of a dict.  Can be used to also 
                  override the name and description properties.
        """
        if description:
            self.description = description
        if name:
            self.name = name
        self.errors = errors or {}

    def get_body(self, environ):
        return json.dumps(dict({'name': self.name, 'description': self.description}.items() + self.errors.items()))

    def get_headers(self, environ):
        return [('Content-Type', 'application/json')]

class Unauthorized(RESTException):
    code = 401
    name = 'Authentication Failed'
    description = 'Please check your credentials and try again. If using an API key, make sure to send it as the "AUTHORIZATION" header with a value of "BASIC <base64 encoded API key>"'

class Forbidden(RESTException):
    code = 403
    name = 'Access Denied'
    description = 'You do not have permission to access this resource.'

class NotFound(RESTException):
    code = 404
    name = 'Not Found'
    description = 'This resource cannot be found. Perhaps it has moved or been deleted?'

class BadRequest(RESTException):
    code = 400
    name = 'Bad Request'
    description = 'Are we speaking the same language? Make sure you sent the right parameters and syntax and try again.'
