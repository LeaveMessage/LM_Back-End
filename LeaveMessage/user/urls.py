from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('emailcheck/', views.email_check),
    path('signup/', views.UserCreate.as_view()),
    path('lifecodecheck/',views.check_lifecode),
    path('lifecode/',views.get_lifecode),
    path('signout/', views.user_signout),
]