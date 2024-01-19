from django import forms
from django.forms import ModelForm
from .models import Radios,Config

class RadioForm(ModelForm):
    class Meta:
        model=Radios
        fields=['id','name','url','state','bandwidth']
        widgets = {
            'name': forms.TextInput(attrs={
            'class': 'nametextbox'
            }),
            'url': forms.TextInput(attrs={
            'class': 'urltextbox'}),
            'bandwidth': forms.TextInput(attrs={
            'class': 'bandwidthtextbox'})
         }

class ConfigForm(ModelForm):
    class Meta:
        model=Config
        fields=['id','frecuency','homelocation','dma_channel']
        widgets = {
            'frecuency': forms.TextInput(attrs={
            'class': 'frecuencytextbox'
            }),
            'homelocation': forms.TextInput(attrs={
            'class': 'homeloctextbox'}),
            'dma_channel': forms.TextInput(attrs={
            'class': 'dma_channelloctextbox'})
         }
