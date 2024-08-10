from django import forms
from .models import UserProfile
from .models import TravelGroup

class NicknameForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname']
        

#초대코드 생성
class InviteCodeForm(forms.Form):
    invite_code = forms.CharField(
        max_length=6,
        label="초대 코드",
        widget=forms.TextInput(attrs={
            'class': 'InviteCodeForm',
            'placeholder': '초대 코드 6자리를 입력해주세요'
        })
    )
