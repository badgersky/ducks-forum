from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    """Registration Form"""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
        })
    )

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
        fields = ('username', 'password', 'confirm_password')

    def clean_confirm_password(self):
        """validate password confirmation"""

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError(f'passwords don`t match')

        return confirm_password

    def clean_username(self):
        """validate username"""

        username = self.cleaned_data.get('username')

        if username and get_user_model().objects.filter(username=username).exists():
            raise ValidationError(f'Try using different username')

        return username

    def save(self, commit=True):
        """set user`s password, save user to database"""

        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.is_active = True

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    """Login Form"""

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def clean_username(self):
        """validate if user - username in database"""

        username = self.cleaned_data.get('username')

        if username and not get_user_model().objects.filter(username=username).exists():
            raise ValidationError(f'No such user, try registering first')

        return username
