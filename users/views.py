from django.shortcuts import render
from django.views import View

from users import forms


class RegistrationView(View):

    def get(self, request):
        form = forms.RegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        pass
