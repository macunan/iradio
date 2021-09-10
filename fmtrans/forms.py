from django import forms
from django.forms import ModelForm
from .models import Radios,Config

class RadioForm(ModelForm):
    class Meta:
        model=Radios
        fields=['id','name','url','state']
        widgets = {
            'name': forms.TextInput(attrs={
            'class': 'px-2 py-1 placeholder-gray-400 text-gray-600 relative bg-white bg-white rounded text-sm border border-gray-400 outline-none focus:outline-none focus:ring w-full'
            }),
            'url': forms.TextInput(attrs={
            'class': 'px-2 py-1 placeholder-gray-400 text-gray-600 relative bg-white bg-white rounded text-sm border border-gray-400 outline-none focus:outline-none focus:ring w-full'})
         }

class ConfigForm(ModelForm):
    class Meta:
        model=Config
        fields=['id','frecuency','homelocation']
        widgets = {
            'frecuency': forms.TextInput(attrs={
            'class': 'px-2 py-1 placeholder-gray-400 text-gray-600 relative bg-white bg-white rounded text-sm border border-gray-400 outline-none focus:outline-none focus:ring w-full'
            }),
            'homelocation': forms.TextInput(attrs={
            'class': 'px-2 py-1 placeholder-gray-400 text-gray-600 relative bg-white bg-white rounded text-sm border border-gray-400 outline-none focus:outline-none focus:ring w-full'})
         }
