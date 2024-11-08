from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name','last_name','email','phone_number','gender')
        widgets = {
            'phone_number': forms.Textarea(attrs={
                'rows': 1,  # 줄 수 조절
                'cols': 20,  # 열 수 조절
                'style': 'resize: both;',  # 사용자가 크기 조절 가능 (가로, 세로)
            })
        }

