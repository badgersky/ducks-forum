from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.DisplayThreadsView.as_view(), name='list'),
    path('create/', views.CreateThreadView.as_view(), name='create'),
    path('<int:pk>/', views.ThreadDetailsView.as_view(), name='details'),
]
