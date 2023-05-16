from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from forum import models


class DisplayThreadsView(ListView):
    model = models.Thread
    template_name = 'forum/list-threads.html'
    context_object_name = 'threads'


class CreateThreadView(LoginRequiredMixin, CreateView):
    model = models.Thread
    fields = ('subject', 'content')
    template_name = 'forum/create-thread.html'
    success_url = reverse_lazy('forum:list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
