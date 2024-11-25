from django.urls import path
from . import views


app_name = "authdemo"

urlpatterns = [
    # ex: authdemo/
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.UserFormView.as_view(), name="register"),
    path("upload", views.file_upload, name="upload"),
]