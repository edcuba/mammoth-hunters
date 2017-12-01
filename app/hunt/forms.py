from ..models import Hunt, Hunter
from django.forms import ModelForm, CheckboxInput, CheckboxSelectMultiple, MultipleChoiceField
from django.forms import BooleanField


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


class HuntDetails(ModelForm):

    deadHunters = MultipleChoiceField(required=False)
    mammothKilled = BooleanField(initial=True, required=False)

    class Meta:
        model = Hunt
        fields = ['target', 'hunters', 'pit', 'circumstances']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        choices = [(hunter.id, hunter) for hunter in self.instance.hunters.all()]

        self.fields['deadHunters'].choices = choices
        self.fields['deadHunters'].label = 'Hunters died'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['mammothKilled'].widget.attrs['class'] = 'flat'
        self.fields['mammothKilled'].label = "Mammoth killed"
