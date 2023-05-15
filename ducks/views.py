from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from _decimal import Decimal

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

            return redirect(reverse('ducks:list'))

        return render(request, 'ducks/add-duck.html', {'form': form})


class ListDucksView(View):
    """lists all ducks with their photos and link to duck-details page"""

    def get(self, request):
        ducks = models.Duck.objects.all()
        duck_table = [ducks[i:i + 3] for i in range(0, len(ducks), 3)]

        return render(request, 'ducks/list-ducks.html', {'duck_table': duck_table})


class DuckDetailsView(View):
    """displays details about a duck"""

    def get(self, request, pk):
        try:
            duck = models.Duck.objects.get(pk=pk)
        except models.Duck.DoesNotExist:
            messages.add_message(request,
                                 messages.WARNING,
                                 f'Sorry, we lost this duck')

            return redirect(reverse('home:home'))

        owner = False

        if request.user.is_authenticated:
            if request.user.id == duck.user.id or request.user.is_superuser:
                owner = True

        overall_stats = ((duck.strength + Decimal(0.2) * duck.avg_weight) +
                         (duck.agility - (Decimal(0.2) * duck.avg_weight)) + duck.intelligence + duck.charisma) / 4
        overall_stats = round(overall_stats, 1)

        return render(request, 'ducks/duck-details.html', {'duck': duck, 'owner': owner, 'overall': overall_stats})


class EditDuckView(View):
    """View for editing duck"""

    def get(self, request, pk):
        try:
            duck = models.Duck.objects.get(pk=pk)
        except models.Duck.DoesNotExist:
            messages.add_message(request,
                                 messages.WARNING,
                                 f'Sorry, we lost this duck')

            return redirect(reverse('home:home'))

        form = forms.EditDuckForm(data={'name': duck.name,
                                        'description': duck.description,
                                        'origin_country': duck.origin_country})
        return render(request, 'ducks/edit-duck.html', {'form': form})

    def post(self, request, pk):
        form = forms.EditDuckForm(request.POST)

        if form.is_valid():
            try:
                duck = models.Duck.objects.get(pk=pk)
            except models.Duck.DoesNotExist:
                messages.add_message(request,
                                     messages.WARNING,
                                     f'Sorry, we lost this duck')

                return redirect(reverse('home:home'))

            duck.name = form.cleaned_data.get('name')
            duck.description = form.cleaned_data.get('description')
            duck.origin_country = form.cleaned_data.get('origin_country')
            duck.save()

            messages.add_message(request,
                                 messages.SUCCESS,
                                 f'Successfully edited duck')

            return redirect(reverse('ducks:list'))


class DeleterDuckView(View):

    def get(self, request, pk):
        if request.user.is_authenticated:
            try:
                duck = models.Duck.objects.get(pk=pk)
            except models.Duck.DoesNotExist:
                messages.add_message(request,
                                     messages.WARNING,
                                     f'Sorry, we lost this duck')

                return redirect(reverse('home:home'))

            if request.user.id == duck.user.id or request.user.is_superuser:
                return render(request, 'ducks/delete-duck.html', {'duck': duck})
            else:
                messages.add_message(request,
                                     messages.WARNING,
                                     f'You cannot delete this duck')

                return redirect(reverse('ducks:details', kwargs={'pk': duck.id}))

        messages.add_message(request,
                             messages.WARNING,
                             f'If you want to delete this duck, you must login')

        return redirect(reverse('users:login'))

    def post(self, request, pk):
        try:
            duck = models.Duck.objects.get(pk=pk)
        except models.Duck.DoesNotExist:
            messages.add_message(request,
                                 messages.WARNING,
                                 f'Sorry, we lost this duck')

            return redirect(reverse('home:home'))

        duck.delete()

        messages.add_message(request,
                             messages.SUCCESS,
                             f'Successfully deleted duck')

        return redirect(reverse('ducks:list'))
