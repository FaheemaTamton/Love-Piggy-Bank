from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['miss_name','mister_name','phone','qr_code','penalty_amount']
