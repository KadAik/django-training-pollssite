from django.urls import path
from . import views


app_name = "authdemo"

urlpatterns = [
    # ex: authdemo/
    path("", views.index, name="index"),
]