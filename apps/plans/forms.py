from django import forms
from .models import UserProfile

class NicknameForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname']