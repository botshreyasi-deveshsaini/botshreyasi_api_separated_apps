
from django import forms
from .models import Uploads

class Uploadforms(forms.ModelForm):
    class Meta:
        model = Uploads
        fields = '__all__'
        labels = {'photo':''}
