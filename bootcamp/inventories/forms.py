from django import forms
from bootcamp.inventories.models import Inventory


class InventoryForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255,help_text='''No spaces are allowes, use '-' instead; eg: new-router''')
    variable = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255,help_text='''Please fill in the router ip where task needs to be run; eg: 10.10.10.102''')
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
        model = Inventory
        fields = ['name', 'description', 'tags', 'status', 'network', 'variable']
