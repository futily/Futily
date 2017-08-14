from django.forms import BaseForm as DjangoBaseForm


class FormMixin(DjangoBaseForm):
    def get_fields(self, fields):
        return [
            field
            for field in self
            if field.name in fields
        ]
