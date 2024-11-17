from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d",
        blank=True,
    )

    def __str__(self):
        return f"Profile for {self.user.username}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Сигнал для создания профиля пользователя
    """
    if created:  # Only create a profile for new users
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Сохранять профиль пользователя при сохранении пользователя.
    Удобно отслеживать время редактирования связанных сущностей.
    """
    instance.profile.save()


class Contact(models.Model):
    user_from = models.ForeignKey(
        verbose_name="Подписчик",
        to="auth.User",
        related_name="rel_from_set",
        on_delete=models.CASCADE,
    )
    user_to = models.ForeignKey(
        verbose_name="Цель подписки",
        to="auth.User",
        related_name="rel_to_set",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name="Дата подписки",
        auto_now_add=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


# Т.к. модель встроенная в django.contrib.auth и менять ее не рекомендуется.
# Добавим M2M поле через add_to_class, а доступ к модели через get_user_model.
User = get_user_model()
User.add_to_class(
    "following",
    models.ManyToManyField(
        to="self",
        through=Contact,
        related_name="followers",
        # Не симметричная связь, если я подписался на вас это
        # не означает, что вы подписались на меня.
        symmetrical=False,
    ),
)
