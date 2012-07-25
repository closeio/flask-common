import csv
import base64

"""
Wrapper around csv reader that ignores non utf-8 chars and strips the record
"""
class CsvReader(object):
    def __init__(self, file_name, delimiter=','):
        self.reader = csv.reader(open(file_name, 'rbU'), delimiter=delimiter)
 
    def __iter__(self):
        return self

    def next(self):
        row = self.reader.next()       
        row = [el.decode('utf8', errors='ignore').replace('\"', '').strip() for el in row]
        return row


def smart_unicode(s, encoding='utf-8', errors='strict'):
    if isinstance(s, unicode):
        return s
    if not isinstance(s, basestring,):
        if hasattr(s, '__unicode__'):
            s = unicode(s)
        else:
            s = unicode(str(s), encoding, errors)
    elif not isinstance(s, unicode):
        s = s.decode(encoding, errors)
    return s

def get_authorization_header(request):
    if 'AUTHORIZATION' in request.headers:
        authorization = request.headers['AUTHORIZATION'].split()
        if len(authorization) == 2 and authorization[0].lower() == 'basic':
            try:
                authorization_parts = base64.b64decode(authorization[1]).partition(':')
                return smart_unicode(authorization_parts[0]), smart_unicode(authorization_parts[2]), True
            except (TypeError, UnicodeDecodeError):
                pass
    return None, None, False
