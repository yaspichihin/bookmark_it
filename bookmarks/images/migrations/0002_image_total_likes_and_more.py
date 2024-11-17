# Generated by Django 5.1.3 on 2024-11-20 20:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="total_likes",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Денормализация количества лайков"
            ),
        ),
        migrations.AddIndex(
            model_name="image",
            index=models.Index(
                fields=["-total_likes"], name="images_imag_total_l_0bcd7e_idx"
            ),
        ),
    ]
