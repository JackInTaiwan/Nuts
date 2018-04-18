from django.urls import path
from . import views



urlpatterns = [
    path("edit_data", views.edit_data),
    path("dump", views.dump_data),
]