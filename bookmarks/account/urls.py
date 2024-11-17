from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [
    path(
        "",
        include("django.contrib.auth.urls"),
        name="dashboard",
    ),
    path(
        "",
        views.dashboard,
        name="dashboard",
    ),
    path(
        "register/",
        views.register,
        name="register",
    ),
    path(
        "edit/",
        views.edit,
        name="edit",
    ),
    path(
        "users/",
        views.user_list,
        name="user_list",
    ),
    path(
        # Должен быть выше, чем "users/<str:username>/".
        "users/follow",
        views.user_follow,
        name="user_follow",
    ),
    path(
        "users/<str:username>/",
        views.user_detail,
        name="user_detail",
    ),
]
