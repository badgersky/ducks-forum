from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from ducks.forms import AddDuckForm, RateDuckForm, EditDuckForm
from ducks.models import Duck, DuckRate
from ducks.permissions import DuckCreatorRequiredMixin


class AddDuckView(LoginRequiredMixin, CreateView):
    """View for adding duck to database"""

    form_class = AddDuckForm
    template_name = 'ducks/add-duck.html'
    context_object_name = 'form'
    success_url = reverse_lazy('ducks:list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.request.user.score = F('score') + 2
        self.request.user.save()
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Successfully added duck')
        return super().get_success_url()

    def handle_no_permission(self):
        messages.add_message(
            self.request,
            messages.WARNING,
            f'Login in order to add duck'
        )
        return super().handle_no_permission()


class ListDucksView(ListView):
    """lists all ducks with their photos and link to duck-details page"""

    model = Duck
    template_name = 'ducks/list-ducks.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        ducks = Duck.objects.all()
        num_of_ducks = ducks.count()
        context['duck_table'] = [ducks[i:i + 3] for i in range(0, num_of_ducks, 3)]

        return context


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
            rates_sum = rates.aggregate(Sum('rate'))
            duck_rate = float(rates_sum['rate__sum']) / rates.count()
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


class EditDuckView(LoginRequiredMixin, DuckCreatorRequiredMixin, UpdateView):
    """View for editing duck"""

    model = Duck
    form_class = EditDuckForm
    template_name = 'ducks/edit-duck.html'
    context_object_name = 'form'
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Successfully edited duck'
        )
        return reverse('ducks:details', kwargs={'pk': self.kwargs.get('pk')})

    def get_login_url(self):
        messages.add_message(
            self.request,
            messages.WARNING,
            f'You must login in order to edit this duck'
        )
        return super().get_login_url()


class DeleteDuckView(LoginRequiredMixin, DuckCreatorRequiredMixin, DeleteView):
    """View for deleting duck"""

    model = Duck
    template_name = 'ducks/delete-duck.html'
    context_object_name = 'duck'
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy('ducks:list')

    def get_login_url(self):
        messages.add_message(
            self.request,
            messages.WARNING,
            f'If you want to delete this duck, you must login'
        )
        return super().get_login_url()

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Successfully deleted duck'
        )
        return super().get_success_url()


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
