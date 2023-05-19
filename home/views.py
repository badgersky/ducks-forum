from django.shortcuts import render
from django.views import View

from forum.models import Thread


class HomeView(View):

    def get(self, request):
        threads = Thread.objects.all().order_by('-likes')
        return render(request, 'home/home.html', {'threads': threads})
