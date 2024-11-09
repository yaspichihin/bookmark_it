from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
)
from .models import Profile


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        template_name="account/dashboard.html",
        context={"section": "dashboard"},
    )


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password1"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(
                request,
                template_name="account/register_done.html",
                context={"new_user": new_user},
            )
    else:
        user_form = UserCreationForm()
    return render(
        request,
        template_name="account/register.html",
        context={"user_form": user_form},
    )


@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST,
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        template_name="account/edit.html",
        context={
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )
