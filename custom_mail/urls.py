from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inbox/', views.inbox, name='inbox'),
    path('<int:message_id>/view/', views.message_view, name='message-view'),
    path('send/', views.message_send, name='message-send'),
    
]
