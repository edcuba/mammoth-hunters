from django.contrib.auth.forms import UserCreationForm
from .models import Hunter


class HunterCreationForm(UserCreationForm):

    class Meta:
        model = Hunter
        fields = ['username', 'password1', 'password2']
