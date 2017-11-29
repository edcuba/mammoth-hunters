from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Hunter


class HunterCreationForm(UserCreationForm):

    class Meta:
        model = Hunter
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']

class HunterChangeForm(ModelForm):
    class Meta:
        model = Hunter
        fields = ['username', 'first_name', 'last_name', 'role',
                  'Strength', 'Stamina', 'Agility', 'Intellect', 'Speed']
    
    def __init__(self, *args, **kwargs):
        super(HunterChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'