from django.urls import path

from . import views


urlpatterns = [
    path('create/', views.create_post),
    path('delete/', views.delete_post),
    path('get/', views.get_post),
    path('update/', views.update_post),
]