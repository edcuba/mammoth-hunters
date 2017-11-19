from django import forms

class TextInput(forms.TextInput):
    """ Styled TextInput widget """
    attrs={'class': 'form-control', 'placeholder': 'Username'}

class PasswordInput(forms.PasswordInput):
    """ Styled PasswordInput widget """
    attrs={'class': 'form-control', 'placeholder': 'Password'}

class LoginForm(forms.Form):
    """ Hunter login form """
    username = forms.CharField(max_length=64, widget=TextInput)
    password = forms.CharField(widget=PasswordInput)
