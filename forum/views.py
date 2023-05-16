from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

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


class ThreadDetailsView(View):

    def get(self, reqeust, pk):
        try:
            thread = models.Thread.objects.get(pk=pk)
        except models.Thread.DoesNotExist:
            messages.add_message(reqeust,
                                 messages.WARNING,
                                 f'No such thread')

            return redirect(reverse('forum:list'))

        comments = models.Comment.objects.filter(thread=thread)

        return render(reqeust, 'forum/thread-details.html', {'thread': thread, 'comments': comments})
