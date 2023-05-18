from django import forms

from .models import Comments


class CommentForm(forms.Form):
    comment_area = forms.CharField(
        label="Комментарий:",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, }),
    )
