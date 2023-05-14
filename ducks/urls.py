from django.urls import path

from . import views

app_name = 'ducks'

urlpatterns = [
    path('add/', views.AddDuckView.as_view(), name='add'),
]
