from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("add/", views.quote, name="add"),
    path("add_author/", views.add_author, name="add_author"),
]
