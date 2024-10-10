# forms.py
from django import forms
from .models import Profil, KodInceleme

class ProfilFotoForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['profil_fotografi']

class KodPaylasForm(forms.ModelForm):
    class Meta:
        model = KodInceleme
        fields = ['kodTitle', 'programlamaDili', 'seoDescription' ,'kodDescription', 'resim']
        widgets = {
            'kodTitle': forms.TextInput(attrs={'class': 'form-control'}),
            'programlamaDili': forms.Select(attrs={'class': 'form-control'}),
            'seoDescription': forms.TextInput(attrs={'class': 'form-control'}),
            'kodDescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resim': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id': 'id_resim'}),
        }