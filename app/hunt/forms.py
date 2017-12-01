from ..models import Hunt, Hunter, Mammoth, Watch, Pit
from django.forms import ModelForm, CheckboxInput, CheckboxSelectMultiple, ModelMultipleChoiceField
from django.forms import BooleanField
from django.db.models import Q


class HuntForm(ModelForm):
    class Meta:
        model = Hunt
        fields = ['target', 'hunters', 'pit']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        watches = Watch.objects.filter(active=True)
        hunts = Hunt.objects.filter(finished=False)
        hunters = Hunter.objects.filter(~Q(watch__in=watches) &
                                        ~Q(hunt__in=hunts) &
                                        Q(killedIn=None))

        pits = Pit.objects.filter(taken=False)
        mammoths = Mammoth.objects.filter(~Q(hunt__in=hunts))
        self.fields['hunters'].queryset = hunters
        self.fields['pit'].queryset = pits
        self.fields['target'].queryset = mammoths
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
