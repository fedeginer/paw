from django.forms import ModelForm
from .models import Auto, Make

class AutoForm(ModelForm):
    class Meta:
        model=Auto
        fields='__all__'

class MakeForm(ModelForm):
    class Meta:
        model=Make
        fields='__all__'