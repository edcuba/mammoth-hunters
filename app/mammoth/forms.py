from django.forms import ModelForm
from ..models import Mammoth


class MammothForm(ModelForm):

    class Meta:
        model = Mammoth
        fields = ['health', 'behavior', 'symbol']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
