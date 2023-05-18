from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from ducks.models import Duck
from users import forms


class RegistrationView(View):
    """Registration View"""

    def get(self, request):
        form = forms.RegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = forms.RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.add_message(request,
                                 messages.SUCCESS,
                                 f'Registration Successful, please login')
            return redirect(reverse('users:login'))

        return render(request, 'users/register.html', {'form': form})


class LoginView(View):
    """Login View"""

    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect(reverse('home:home'))

        return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    """Logout View"""

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

        return redirect(reverse('home:home'))


class AddFavDuck(View):

    def get(self, request, pk):
        if request.user.is_authenticated:
            try:
                duck = Duck.objects.get(pk=pk)
            except Duck.DoesNotExist:
                messages.add_message(request,
                                     messages.WARNING,
                                     f'This duck does not exist')

                return redirect(reverse('ducks:list'))

            request.user.fav_ducks.add(duck)

            return redirect(reverse('ducks:details', kwargs={'pk': pk}))

        messages.add_message(request,
                             messages.WARNING,
                             f'Login if you want to add this duck to favorites')

        return redirect(reverse('users:login'))
    