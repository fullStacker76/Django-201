from django import forms
from django.contrib.auth import get_user_model
from betterforms.multiform import MultiModelForm
from .models import Profile

User = get_user_model()
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)

class UserProfileMultiForm(MultiModelForm):
    form_classes = {
        'user': UserEditForm,
        'profile': UserProfileForm,
    }