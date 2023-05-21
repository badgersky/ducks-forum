from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView

from ducks.forms import AddDuckForm, RateDuckForm, EditDuckForm
from ducks.models import Duck, DuckRate


class AddDuckView(LoginRequiredMixin, CreateView):
    """View for adding duck to database"""

    form_class = AddDuckForm
    template_name = 'ducks/add-duck.html'
    context_object_name = 'form'
    success_url = reverse_lazy('ducks:list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.request.user.score = F('score') + 1
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Successfully added duck')
        return super().get_success_url()

    def handle_no_permission(self):
        messages.add_message(self.request,
                             messages.WARNING,
                             f'Login in order to add duck'
                             )
        return super().handle_no_permission()


class ListDucksView(View):
    """lists all ducks with their photos and link to duck-details page"""

    def get(self, request):
        ducks = Duck.objects.all()
        duck_table = [ducks[i:i + 3] for i in range(0, len(ducks), 3)]

        return render(request, 'ducks/list-ducks.html', {'duck_table': duck_table})


class DuckDetailsView(View):
    """displays details about a duck"""

    def get(self, request, pk):
        try:
            duck = Duck.objects.get(pk=pk)
        except Duck.DoesNotExist:
            messages.add_message(request,
                                 messages.WARNING,
                                 f'Sorry, we lost this duck')

            return redirect(reverse('home:home'))

        owner = False
        favorite = False

        if request.user.is_authenticated:
            if request.user.id == duck.user.id or request.user.is_superuser:
                owner = True
            if duck in request.user.fav_ducks.all():
                favorite = True

        rates = DuckRate.objects.filter(duck=duck)
        if rates:
            rates_values = [rate.rate for rate in rates]
            duck_rate = sum(rates_values) / len(rates_values)
            duck_rate = round(duck_rate, 1)
        else:
            duck_rate = 0

        overall_stats = (duck.strength + duck.agility + duck.intelligence + duck.charisma) / 4
        overall_stats = round(overall_stats, 1)

        rate_form = RateDuckForm()

        return render(request, 'ducks/duck-details.html', {'duck': duck,
                                                           'owner': owner,
                                                           'overall': overall_stats,
                                                           'form': rate_form,
                                                           'rate': duck_rate,
                                                           'favorite': favorite,
                                                           })


class EditDuckView(View):
    """View for editing duck"""

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
                form = forms.EditDuckForm(initial={'name': duck.name,
                                                   'description': duck.description,
                                                   'origin_country': duck.origin_country,
                                                   'avg_weight': duck.avg_weight,
                                                   'strength': duck.strength,
                                                   'agility': duck.agility,
                                                   'intelligence': duck.intelligence,
                                                   'charisma': duck.charisma})

                return render(request, 'ducks/edit-duck.html', {'form': form})
            else:
                messages.add_message(request,
                                     messages.WARNING,
                                     f'You cannot edit this duck')

                return redirect(reverse('ducks:details', kwargs={'pk': duck.id}))

        messages.add_message(request,
                             messages.WARNING,
                             f'If you want to edit this duck, you must login')

        return redirect(reverse('users:login'))

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
            duck.avg_weight = form.cleaned_data.get('avg_weight')
            duck.strength = form.cleaned_data.get('strength')
            duck.agility = form.cleaned_data.get('agility')
            duck.intelligence = form.cleaned_data.get('intelligence')
            duck.charisma = form.cleaned_data.get('charisma')
            duck.save()

            messages.add_message(request,
                                 messages.SUCCESS,
                                 f'Successfully edited duck')

            return redirect(reverse('ducks:list'))

        messages.add_message(request,
                             messages.WARNING,
                             f'No edits have been made')

        return redirect(reverse('ducks:details', kwargs={'pk': pk}))


class DeleteDuckView(View):
    """View for deleting duck"""

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


class RateDuckView(View):

    def post(self, request, pk):
        try:
            duck = models.Duck.objects.get(pk=pk)
        except models.Duck.DoesNotExist:
            messages.add_message(request,
                                 messages.WARNING,
                                 f'Sorry, we lost this duck')

            return redirect(reverse('home:home'))

        if request.user.is_authenticated:
            form = forms.RateDuckForm(request.POST)

            if form.is_valid():
                if models.DuckRate.objects.filter(user=request.user, duck=duck).exists():
                    messages.add_message(request,
                                         messages.WARNING,
                                         f'You have already rated {duck.name.title()}')

                    return redirect(reverse('ducks:details', kwargs={'pk': pk}))

                rate = form.save(commit=False)

                rate.user = request.user
                rate.duck = duck

                form.save()

                return redirect(reverse('ducks:details', kwargs={'pk': pk}))

        messages.add_message(request,
                             messages.WARNING,
                             f'Login before rating {duck.name.title()}')

        return redirect(reverse('users:login'))
