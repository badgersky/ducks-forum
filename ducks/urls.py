from django.urls import path

from . import views

app_name = 'ducks'

urlpatterns = [
    path('add/', views.AddDuckView.as_view(), name='add'),
    path('list/', views.ListDucksView.as_view(), name='list'),
    path('<int:pk>/', views.DuckDetailsView.as_view(), name='details'),
    path('edit/<int:pk>/', views.EditDuckView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.DeleteDuckView.as_view(), name='delete'),
]
