from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.wiki, name="index_start"),
    path("wiki/<str:entry>", views.wiki, name="wiki"),
    path("search/", views.search, name="search")
]
