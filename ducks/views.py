from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from ducks import forms, models


class AddDuckView(View):
    """View for adding duck to database"""

    def get(self, request):
        if request.user.is_authenticated:
            form = forms.AddDuckForm()
            return render(request, 'ducks/add-duck.html', {'form': form})

        messages.add_message(request,
                             messages.WARNING,
                             f'Login in order to add duck'
                             )
        return redirect(reverse('users:login'))

    def post(self, request):
        form = forms.AddDuckForm(request.POST, request.FILES)

        if form.is_valid():
            duck = form.save(commit=False)

            duck.user = request.user
            duck.save()

            messages.add_message(request,
                                 messages.SUCCESS,
                                 f'Successfully added duck')

            return redirect(reverse('home:home'))

        return render(request, 'ducks/add-duck.html', {'form': form})


class ListDucksView(View):
    """lists all ducks with their photos and link to duck-details page"""

    def get(self, request):
        ducks = models.Duck.objects.all()
        duck_table = [ducks[i:i+3] for i in range(0, len(ducks), 3)]

        return render(request, 'ducks/list-ducks.html', {'duck_table': duck_table})
