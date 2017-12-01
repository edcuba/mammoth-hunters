from ..models import Hunt, Hunter
from django.forms import ModelForm, CheckboxInput, CheckboxSelectMultiple, ModelMultipleChoiceField
from django.forms import BooleanField


class HuntForm(ModelForm):
    class Meta:
        model = Hunt
        fields = ['target', 'hunters', 'pit']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class HuntDetails(ModelForm):

    deadHunters = ModelMultipleChoiceField(queryset=Hunter.objects.all(), required=False)
    mammothKilled = BooleanField(initial=True, required=False)

    class Meta:
        model = Hunt
        fields = ['target', 'hunters', 'pit', 'circumstances', 'finished']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['deadHunters'].label = 'Hunters died'
        self.fields['deadHunters'].queryset = self.instance.hunters.all()

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['mammothKilled'].widget.attrs['class'] = 'flat'
        self.fields['mammothKilled'].label = "Mammoth killed"

        if 'finished' in self.fields:
            self.fields['finished'].widget.attrs['class'] = 'flat'


class HuntSubmit(HuntDetails):
    class Meta:
        model = Hunt
        fields = ['circumstances']
