from django.urls import path
from . import views

urlpatterns = [
    path('', views.form),
    path('registered', views.registered),
    path('logout', views.logout),
    path('login', views.login),
    path('success', views.success),
]