from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
        })
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'confirm_password')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError(f'passwords don`t match')

        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username and get_user_model().objects.filter(username=username).exists():
            raise ValidationError(f'Try using different username')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and get_user_model().objects.filter(email=email).exists():
            raise ValidationError(f'Try using different email')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()
            user.is_active = True

        return user
