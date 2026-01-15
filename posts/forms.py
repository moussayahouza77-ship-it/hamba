from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titre', 'categorie', 'contenu', 'image', 'actif']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows':6}),
        }
