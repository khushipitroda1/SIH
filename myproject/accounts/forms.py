from django import forms
from .models import *


class otp_match_form(forms.ModelForm):
    otp = forms.CharField(max_length = 6, widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Your OTP'}))