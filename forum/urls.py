from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.DisplayThreadsView.as_view(), name='list'),
    path('create/', views.CreateThreadView.as_view(), name='create'),
    path('<int:pk>/', views.ThreadDetailsView.as_view(), name='details'),
    path('add-comment/<int:pk>/', views.AddCommentView.as_view(), name='add-comment'),
    path('delete-thread/<int:pk>/', views.DeleteThreadView.as_view(), name='delete-thread'),
    path('delete-comment/<int:pk>/', views.DeleteCommentView.as_view(), name='delete-comment'),
]
