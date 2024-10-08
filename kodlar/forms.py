# forms.py
from django import forms
from .models import Profil

class ProfilFotoForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['profil_fotografi']