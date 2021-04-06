from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'website_url')

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
        }