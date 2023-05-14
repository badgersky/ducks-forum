from django.contrib import messages
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
            return redirect(reverse('home:home'))

        return render(request, 'users/register.html', {'form': form})
