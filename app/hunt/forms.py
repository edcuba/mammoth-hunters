from ..models import Hunt
from django.forms import ModelForm, CheckboxInput, CheckboxSelectMultiple


class HuntForm(ModelForm):
    class Meta:
        model = Hunt
        fields = ['target', 'hunters', 'pit']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class HuntSubmit(HuntForm):
    class Meta:
        model = Hunt
        fields = ['target', 'hunters', 'circumstances']

    def __init__(self, *args, **kwargs):
        super(HuntForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['target'].widget = CheckboxInput(attrs={'class': 'flat'})
        self.fields['target'].label = 'Mammoth killed'
        self.fields['hunters'].widget = CheckboxSelectMultiple(attrs={'class': 'flat'})
        self.fields['hunters'].label = 'Hunters survived'
        self.fields['hunters'].queryset = self.instance.hunters.all()
