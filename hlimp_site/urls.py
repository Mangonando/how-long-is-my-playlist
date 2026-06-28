from django.urls import include, path

urlpatterns = [path("", include("playlists.urls"))]
