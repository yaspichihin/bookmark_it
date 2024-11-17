# Generated by Django 5.1.3 on 2024-11-11 22:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=200, verbose_name="Заголовок изображения"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=200, verbose_name="Красивый URL-адрес"
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        max_length=2000,
                        verbose_name="Изначальный URL-адрес изображения",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="images/%Y/%m/%d", verbose_name="Изображения"
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                (
                    "created",
                    models.DateField(auto_now_add=True, verbose_name="Дата добавления"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь чье изображение",
                    ),
                ),
                (
                    "users_like",
                    models.ManyToManyField(
                        blank=True,
                        related_name="images_liked",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created",),
                "indexes": [
                    models.Index(
                        fields=["-created"], name="images_imag_created_d57897_idx"
                    )
                ],
            },
        ),
    ]
