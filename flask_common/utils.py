import csv
import base64
from logging.handlers import SMTPHandler


class DetailedSMTPHandler(SMTPHandler):
    def __init__(self, app_name, *args, **kwargs):
        self.app_name = app_name
        return super(DetailedSMTPHandler, self).__init__(*args, **kwargs)

    def getSubject(self, record):
        from flask import request
        from socket import gethostname
        error = 'Error'
        ei = record.exc_info
        if ei:
            error = '(%s) %s' % (ei[0].__name__, ei[1])
        return "[%s] %s %s on %s" % (self.app_name, request.path, error, gethostname())

    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            from email.utils import formatdate
            from flask import request
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s\n\nRequest.url: %s\n\nRequest.headers: %s\n\nRequest.args: %s\n\nRequest.form: %s\n\nRequest.data: %s\n" % (
                            self.fromaddr,
                            ",".join(self.toaddrs),
                            self.getSubject(record),
                            formatdate(), msg, request.url, request.headers, request.args, request.form, request.data)
            if self.username:
                if self.secure is not None:
                    smtp.ehlo()
                    smtp.starttls(*self.secure)
                    smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

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


class Enum(object):
    @classmethod
    def choices(cls):
        return [(getattr(cls,v), v) for v in dir(cls) if not callable(getattr(cls,v)) and not (v.startswith('__') and v.endswith('__'))]

def grouper(n, iterable):
    # e.g. 2, [1, 2, 3, 4, 5] -> [[1, 2], [3, 4], [5]]
    return [iterable[i:i+n] for i in range(0, len(iterable), n)]
