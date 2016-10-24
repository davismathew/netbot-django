from django import forms
from bootcamp.results.models import Result


class ResultForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    variable = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    MULTIPLECHOICES=[('EMC','EMC'),
         ('MTN','MTN'),('Both','Both')]
    network = forms.ChoiceField(choices=MULTIPLECHOICES, widget=forms.RadioSelect(),
                                         help_text='Mention the network in which task is expected to run')
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False,
        help_text='Use spaces to separate the tags, such as "interfaces emc automation"')

    class Meta:
        model = Result
        fields = ['name', 'description', 'tags', 'status', 'network', 'variable']
