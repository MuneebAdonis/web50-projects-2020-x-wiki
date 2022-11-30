from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page_entry, name="page_entry"),
    path("results", views.results, name= "results"),
    path("new_page", views.new_page, name = "new_page"),
    path("edit/<str:title>", views.edit, name= "edit"),
    path("random",views.random, name= "random")
]
