from django import forms
from bootcamp.confcreator.models import ConfCreator




class ConfCreatorForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    # template = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=255,
    #     help_text='Please do not use spaces in between, use "_" instead"')
    commands = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=255)
    # description = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}))
    # playbook = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=255)
    MULTIPLECHOICES=[('EMC','EMC'),
         ('MTN','MTN'),('Both','Both')]
    network = forms.ChoiceField(choices=MULTIPLECHOICES, widget=forms.RadioSelect(),
                                         help_text='Mention the network in which task is expected to run')

    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False,
        help_text='Use spaces to separate the tags, such as "interfaces emc automation"')
    # jinjafile = forms.FileField(label="Upload the jinja file with 'j2' as extension",required=False)
    # variablefile = forms.FileField(label="Upload the variable file with 'txt' as extension",required=False)
    # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = ConfCreator
        fields = ['name', 'commands', 'tags']
