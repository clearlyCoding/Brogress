from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path("", views.homepage, name = "homepage"),
    path("update", views.update, name = "update"),
    path("register",views.register, name = "register"),
    path("logout", views.logout_request, name = "logout"),
    path("login", views.login_request, name = "login")
   
]
