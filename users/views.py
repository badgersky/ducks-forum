from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from users import forms


class RegistrationView(View):

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
