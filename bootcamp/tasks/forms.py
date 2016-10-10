from django import forms
from bootcamp.tasks.models import Task


class TaskForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    CHOICES=[('true','True'),
         ('false','False')]
    factfilerequired = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),
                                         help_text='Mention if the task requires a factfile to run')
    MULTIPLECHOICES=[('EMC','EMC'),
         ('MTN','MTN'),('Both','Both')]
    network = forms.ChoiceField(choices=MULTIPLECHOICES, widget=forms.RadioSelect(),
                                         help_text='Mention the network in which task is expected to run')
    playbook = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    credential = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False)
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False,
        help_text='Use spaces to separate the tags, such as "interfaces emc automation"')

    class Meta:
        model = Task
        fields = ['name', 'description', 'tags', 'status', 'network', 'playbook', 'credential', 'factfilerequired']
