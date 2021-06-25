from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Post, Comment, Rating


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'website_url')

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating',)

        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
        }