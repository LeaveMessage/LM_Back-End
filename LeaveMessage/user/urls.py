from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    #path('emailcheck/', 'pass'),
    path('signup/', views.UserCreate.as_view()),
    #path('lifecode/', 'pass'),
    #path('signout/', 'pass'),
]