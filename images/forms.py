from django import forms
from .models import Image


class ImageCreateForm:
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgets = {
            "url": forms.HiddenInput
        }

    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png"]
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("This url address does not contains an image in the allowed format")
        return url
