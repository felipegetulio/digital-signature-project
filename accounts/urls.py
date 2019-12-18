from django.urls import path, re_path

from . import views


urlpatterns = [
    #path('signup/', views.SignUp.as_view(), name='signup'),
    re_path(r'^signup/$', views.signup, name='signup'),
]