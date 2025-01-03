# Generated by Django 5.1.3 on 2024-11-19 23:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Action",
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
                ("verb", models.CharField(max_length=255, verbose_name="Действие")),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата действия"
                    ),
                ),
                (
                    "target_id",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Первичный ключ связанного объекта",
                    ),
                ),
                (
                    "target_ct",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="target_obj",
                        to="contenttypes.contenttype",
                        verbose_name="Модель объекта",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="actions",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
                "indexes": [
                    models.Index(
                        fields=["-created"], name="actions_act_created_64f10d_idx"
                    ),
                    models.Index(
                        fields=["target_ct", "target_id"],
                        name="actions_act_target__f20513_idx",
                    ),
                ],
            },
        ),
    ]
