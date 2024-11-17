from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey(
        verbose_name="Пользователь",
        to=settings.AUTH_USER_MODEL,
        related_name="actions",
        on_delete=models.CASCADE,
    )
    verb = models.CharField(
        verbose_name="Действие",
        max_length=255,
    )
    created = models.DateTimeField(
        verbose_name="Дата действия",
        auto_now_add=True,
    )
    target_ct = models.ForeignKey(
        verbose_name="Модель объекта",
        to=ContentType,
        related_name="target_obj",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    target_id = models.PositiveIntegerField(
        verbose_name="Первичный ключ связанного объекта",
        blank=True,
        null=True,
    )
    target = GenericForeignKey(
        # Связанный объект на базе target_ct и target_id
        ct_field="target_ct",
        fk_field="target_id",
    )

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["target_ct", "target_id"]),
        ]
        ordering = ["-created"]
