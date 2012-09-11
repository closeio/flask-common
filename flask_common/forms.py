from flask.ext.mongoengine import wtf
from flask.ext.admin.contrib.mongoengine.view import AdminModelForm, AdminModelConverter
from flask.ext.mongoengine.wtf.orm import converts
from flask.ext.common.formfields import BetterDateTimeField

from wtforms import fields


class ModelConverter(AdminModelConverter):
    def __init__(self, *args, **kwargs):
        self.expand_references = kwargs.pop('expand_references', {})
        #super(ModelConverter, self).__init__(*args, **kwargs)
        AdminModelConverter.__init__(self, *args, **kwargs)

    @converts('ReferenceField')
    def conv_Reference(self, model, field, kwargs):
        for field_name, form_class in self.expand_references.iteritems():
            the_field = getattr(model, field_name)
            if the_field == field or getattr(the_field, 'field', None) == field:
                if form_class:
                    def get_form_class(*args, **kwargs):
                        kwargs['csrf_enabled'] = False
                        return form_class(*args, **kwargs)

                    return fields.FormField(get_form_class, {'validators': [], 'filters': []})
                else:
                    return self.conv_EmbeddedDocument(model, field, kwargs)

        #return super(ModelConverter, self).conv_Reference(model, field, kwargs)
        return AdminModelConverter.conv_Reference(self, model, field, kwargs)

    @converts('ListField')
    def conv_List(self, model, field, kwargs):
        for field_name in self.expand_references:
            if getattr(model, field_name) == field:

                unbound_field = self.convert(model, field.field, {})
                kwargs = {
                    'validators': [],
                    'filters': [],
                }
                return fields.FieldList(unbound_field, min_entries=0, **kwargs)

        else:
            #return super(ModelConverter, self).conv_List(model, field, kwargs)
            return AdminModelConverter.conv_List(self, model, field, kwargs)

    @converts('PhoneField')
    def conv_Phone(self, model, field, kwargs):
        return self.conv_String(model, field, kwargs)

    @converts('TrimmedStringField')
    def conv_TrimmedString(self, model, field, kwargs):
        return self.conv_String(model, field, kwargs)

    @converts('DateTimeField')
    def conv_DateTime(self, model, field, kwargs):
        return BetterDateTimeField(**kwargs)

def model_form(*args, **kwargs):
    expand_references = kwargs.pop('expand_references', {})
    kwargs['base_class'] = AdminModelForm
    kwargs['converter'] = ModelConverter(expand_references=expand_references)
    kwargs['exclude'] = kwargs.get('exclude', []) + ['id']

    return wtf.model_form(*args, **kwargs)
