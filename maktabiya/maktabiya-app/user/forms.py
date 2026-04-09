from django.contrib.auth import get_user_model
from django import forms
from django.forms.widgets import ClearableFileInput as BaseClearableFileInput


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ClearableFileInput(BaseClearableFileInput):
    initial_text = ""
    input_text = "Upload new avatar"
    template_name = "user/clearable_input.html"


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=ClearableFileInput(), required=False)

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "avatar", "booking_visible"]
