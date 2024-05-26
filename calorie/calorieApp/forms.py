from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from calorieApp import models

class SignUp(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=30)
    class Meta:
        model=User
        model._meta.get_field('email')._unique=True
        fields=('username','first_name','last_name','email','password1','password2')

class UserDetailForm(forms.ModelForm):
    class Meta:
        model=models.UserDetails
        fields=('name','age','height','weight','gender','activity_factor')

class AddItemForm(forms.ModelForm):
    class Meta:
        model=models.AddItems
        fields=('user','food','quantity','meal_time')

