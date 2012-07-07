from flask.ext.mongoengine import wtf
from flask.ext.admin.contrib.mongoengine.view import AdminModelForm, AdminModelConverter
from flask.ext.mongoengine.wtf.orm import converts


class ModelConverter(AdminModelConverter):
    @converts('PhoneField')
    def conv_Phone(self, model, field, kwargs):
        return self.conv_String(model, field, kwargs)

def model_form(*args, **kwargs):
    kwargs['base_class'] = AdminModelForm
    kwargs['converter'] = ModelConverter()
    kwargs['exclude'] = kwargs.get('exclude', []) + ['id']

    return wtf.model_form(*args, **kwargs)
