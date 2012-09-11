import dateutil.parser
from wtforms.fields import DateTimeField

class BetterDateTimeField(DateTimeField):
    """ Like DateTimeField, but uses dateutil.parser to parse the date """

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = u' '.join(valuelist)
            try:
                self.data = dateutil.parser.parse(date_str)
            except ValueError:
                self.data = None
                raise
