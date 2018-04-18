from django.urls import path
from Weather import views



urlpatterns = [
    path("get", views.get_whether),
]