from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    referral_code = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "display_name",
            "email",
            "role",
            "referral_code",
            "password1",
            "password2",
        ]
