from django.shortcuts import render
from django.views.generic import CreateView, ListView

from forum import models


class DisplayThreadsView(ListView):
    model = models.Thread
    template_name = 'forum/list-threads.html'
    context_object_name = 'threads'
