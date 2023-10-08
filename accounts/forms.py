from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser  

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    profile_image = forms.ImageField() 

    class Meta:
        model = CustomUser 
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'profile_image']
        

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data