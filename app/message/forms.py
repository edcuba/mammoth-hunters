from django.forms import ModelForm, CheckboxSelectMultiple
from ..models import Message


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ['mammoths']
        widgets = {'mammoths': CheckboxSelectMultiple(attrs={'class': 'flat'})}
