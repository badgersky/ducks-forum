from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from forum.models import Thread


class HomeView(View):

    def get(self, request):
        threads = Thread.objects.all().order_by('-likes')

        paginator = Paginator(threads, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home/home.html', {'page_obj': page_obj})
