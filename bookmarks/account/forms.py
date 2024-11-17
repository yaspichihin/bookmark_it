from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "email",
        ]

    def clean_password2(self):
        """
        Валидация и очистка поля при отсутствии ошибок.
        Вызывается автоматически при методе is_valid из-за
        префикса 'clean_'.
        """
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"]

        # fmt: off
        is_duplicate_email = (
            User.objects
            .exclude(id=self.instance.id)
            .filter(email=email)
        )
        # fmt: on

        if is_duplicate_email.exists():
            raise forms.ValidationError("Email already in use.")

        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]
