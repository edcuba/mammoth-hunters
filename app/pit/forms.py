from django.forms import ModelForm
from ..models import Pit

class PitForm(ModelForm):
    class Meta:
        model = Pit
        fields = ['location']
    
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs['class'] = 'form-control'

