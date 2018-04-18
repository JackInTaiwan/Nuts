from django.urls import path
from . import views


urlpatterns = [
    path("edit_data", views.edit_data),
    path("event", views.event),
    path("change_comment", views.change_comment),
    path("dump", views.dump_data),
    path("get_location", views.get_location),
]