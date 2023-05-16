from django import forms

from forum import models


class AddCommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'width': 300,
            'height': 50,
            'placeholder': 'Write a comment',
        })
    )

    class Meta:
        model = models.Comment
        fields = ('content',)
