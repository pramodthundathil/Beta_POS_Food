from django.urls import path 
from .import views  

from django.contrib.auth.views import LogoutView

urlpatterns = [

    path("Index",views.Index,name="Index"),
    path('',views.SignIn,name="SignIn"),
    path('SignOut', views.SignOut, name='SignOut'),
]