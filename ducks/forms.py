from django import forms

from ducks import models


class AddDuckForm(forms.ModelForm):
    """Add Duck Form"""

    class Meta:
        model = models.Duck
        fields = ('name',
                  'description',
                  'origin_country',
                  'image',
                  'avg_weight',
                  'strength',
                  'agility',
                  'intelligence',
                  'charisma')
