from django import forms
from django.forms import ModelForm
from .models import Radios,Config

class RadioForm(ModelForm):
    class Meta:
        model=Radios
        fields=['id','name','url','state']
        widgets = {
            'name': forms.TextInput(attrs={
            'class': 'nametextbox'
            }),
            'url': forms.TextInput(attrs={
            'class': 'urltextbox'})
         }

class ConfigForm(ModelForm):
    class Meta:
        model=Config
        fields=['id','frecuency','homelocation','wavlocation','dma_channel','bandwidth']
        widgets = {
            'frecuency': forms.TextInput(attrs={
            'class': 'frecuencytextbox'
            }),
            'homelocation': forms.TextInput(attrs={
            'class': 'homeloctextbox'}),
            'wavlocation': forms.TextInput(attrs={
            'class': 'wavloctextbox'}),
            'dma_channel': forms.TextInput(attrs={
            'class': 'dma_channelloctextbox'}),
            'bandwidth': forms.TextInput(attrs={
            'class': 'bandwidthloctextbox'})
         }
