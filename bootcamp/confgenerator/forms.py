from django import forms
from bootcamp.confgenerator.models import ConfTemplate
from bootcamp.confgenerator.models import ConfTemplateInstance

temp="this is the help text"
class ConfForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('variables')
        super(ConfForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            self.fields[question] = forms.CharField(label=question)
            # self.fields['name'].widget=forms.HiddenInput()
    class Meta:
        model = ConfTemplateInstance
        fields = ['name']



class ConfTemplateForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    template = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255,
        help_text='Please do not use spaces in between, use "_" instead"')
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    # playbook = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=255)
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False,
        help_text='Use spaces to separate the tags, such as "interfaces emc automation"')
    file = forms.FileField()

    class Meta:
        model = ConfTemplate
        fields = ['name', 'description', 'tags']
