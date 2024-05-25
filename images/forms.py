from django import forms

class ImageCreateForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        label='Title',
        required=True,
    )
    image = forms.ImageField(
        label='Upload file',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        }),
        required=True,
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea,
        required=False,
    )
