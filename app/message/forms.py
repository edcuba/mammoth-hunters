from django.forms import ModelForm, CheckboxSelectMultiple, Textarea, TextInput
from ..models import Message


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ['mammoths', 'text', 'title']
        widgets = {'mammoths': CheckboxSelectMultiple(attrs={'class': 'flat'}),
                   'text': Textarea(attrs={'class': 'form-control'}),
                   'title': TextInput(attrs={'class': 'form-control'})}
