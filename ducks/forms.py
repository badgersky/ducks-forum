from django import forms
from django.core.exceptions import ValidationError

from ducks import models


class AddDuckForm(forms.ModelForm):
    """Add Duck Form"""

    origin_country = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'If unknown, leave blank'
        })
    )

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

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if name and models.Duck.objects.filter(name=name.lower()).exists():
            raise ValidationError(f'This duck already in database')

        return name.lower()

    def clean_origin_country(self):
        origin_country = self.cleaned_data.get('origin_country')

        if not origin_country:
            return 'Unknown'

        return origin_country

    def save(self, commit=True):
        duck = super().save(commit=False)
        duck.origin_country = self.clean_origin_country()
        duck.name = self.cleaned_data.get('name').lower()

        if commit:
            super().save()

        return duck


class EditDuckForm(AddDuckForm):
    """class for editing duck"""

    class Meta(AddDuckForm.Meta):
        fields = ('name',
                  'description',
                  'origin_country',
                  'avg_weight',
                  'strength',
                  'agility',
                  'intelligence',
                  'charisma')


class RateDuckForm(forms.ModelForm):
    choices = []
    for i in range(1, 11):
        choices.append((i, '\N{white medium star}' * i))

    rate = forms.ChoiceField(
        label='Rate Duck',
        choices=choices
        )

    class Meta:
        model = models.DuckRate
        fields = ('rate',)
