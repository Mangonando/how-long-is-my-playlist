from django.urls import path

from . import views

urlpatterns = [
    path("", views.calculator, name="calculator"),
    path("login/", views.spotify_login, name="spotify_login"),
    path("callback/", views.spotify_callback, name="spotify_callback"),
    path("logout/", views.spotify_logout, name="spotify_logout"),
]
