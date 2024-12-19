from django.urls import path
from .import views

urlpatterns = [
    path("callback/", views.message_handle, name="line-callback"),
]