from django import forms
from froala_editor.widgets import FroalaEditor

from news.models import Comment


class CommentForm(forms.ModelForm):
    description = forms.CharField(widget=FroalaEditor)

    class Meta:
        model = Comment
        fields = ('description',)
