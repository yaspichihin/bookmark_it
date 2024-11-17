from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from actions.utils import create_action
from actions.models import Action
from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
)
from .models import Contact

# Определение модели User в django.contrib.auth
User = get_user_model()


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:

    # Подготовить действия всех пользователей по умолчанию.
    # Кроме действий самого пользователя.
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list("id", flat=True)

    # Если у пользователя есть подписки, то подготовить их действия.
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)

    # Выбрать последние 10 действий. Сортировка по умолчанию из Meta.
    # fmt: off
    actions = (
        actions
        .select_related("user", "user__profile")
        .prefetch_related("target")
        [:10]
    )
    # fmt: on

    return render(
        request=request,
        template_name="account/dashboard.html",
        context={
            "section": "dashboard",
            "actions": actions,
        },
    )


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password1"])
            new_user.save()
            create_action(new_user, "has created a new account")
            return render(
                request=request,
                template_name="account/register_done.html",
                context={
                    "new_user": new_user,
                },
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request=request,
        template_name="account/register.html",
        context={
            "user_form": user_form,
        },
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
            # profile_form.save()
            messages.success(
                request=request,
                message="Profile updated successfully",
            )
        else:
            messages.error(
                request=request,
                message="Error updating your profile",
            )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request=request,
        template_name="account/edit.html",
        context={
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


@login_required
def user_list(request: HttpRequest) -> HttpResponse:
    users = User.objects.filter(is_active=True)
    return render(
        request=request,
        template_name="account/user/list.html",
        context={
            "section": "people",
            "users": users,
        },
    )


@login_required
def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(
        User,
        username=username,
        is_active=True,
    )
    return render(
        request=request,
        template_name="account/user/detail.html",
        context={
            "section": "people",
            "user": user,
        },
    )


@require_POST
@login_required
def user_follow(request: HttpRequest) -> HttpResponse:
    user_id = request.POST.get("id")
    action = request.POST.get("action")

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user,
                )
                create_action(request.user, "is following", user)

            elif action == "unfollow":
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user,
                ).delete()
            return JsonResponse({"status": "ok"})

        except User.DoesNotExist:
            return JsonResponse({"status": "error"})

    return JsonResponse({"status": "error"})
