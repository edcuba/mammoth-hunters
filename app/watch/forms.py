from django.forms import ModelForm
from ..models import Watch

class WatchForm(ModelForm):
    class Meta:
        model = Watch
        fields = ['location', 'hunters']
    
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

