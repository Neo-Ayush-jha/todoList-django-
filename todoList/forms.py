from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
class SingupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=User
        fields=('username','first_name','last_name','email')
    def save(self,commit=True):
        user=super().save(commit=False)
        user.is_public=True
        if commit:
            user.save()
        return user
class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        exclude=("user","created_at",)