from django.contrib.auth.forms import PasswordChangeForm

class PasswdForm(PasswordChangeForm):
    """ Style password change form """

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
