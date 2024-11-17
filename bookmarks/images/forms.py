from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
import requests

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgets = {
            "url": forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extensions = ("jpg", "jpeg", "png")
        _, extension = url.lower().rsplit(sep=".", maxsplit=1)
        print(extension)

        if extension not in valid_extensions:
            err = "The given URL does not match valid image extension."
            raise forms.ValidationError(err)

        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        _, extension = image_url.lower().rsplit(sep=".", maxsplit=1)
        image_name = f"{name}.{extension}"

        # Скачать изображение
        response = requests.get(image_url)
        image.image.save(
            image_name,
            ContentFile(response.content),
            save=False,
        )

        if commit:
            image.save()

        return image
