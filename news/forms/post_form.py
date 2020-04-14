from django import forms
from froala_editor.widgets import FroalaEditor

from news.models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True,
                            help_text='Please provide title for your post',
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'post-title',
                                    'placeholder': 'Title',
                                }))
    description = forms.CharField(widget=FroalaEditor)

    class Meta:
        model = Post
        fields = ('title', 'description')
