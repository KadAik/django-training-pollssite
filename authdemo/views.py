import shutil
import time

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from .models import User, FileUploadTracker
from django.views import View
from .forms import UserForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .tasks import handle_file_upload_task
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import pathlib
import os
import json
from django.db.models import F


# Create your views here.

def index(request):
    template = "authdemo/home.html"
    return render(request, template, context={"user": request.session.user, "request": request, "body_class": "home"})


def login(request):
    next_url = request.GET.get("next")

    error_message = {}

    if request.method == "POST":
        user_firstname = request.POST.get("first-name")
        user_password = request.POST.get("password")

        try:
            # Fetching the user by its first name
            user = User.objects.filter(first_name=user_firstname).first()
        except User.DoesNotExist:
            error_message["name"] = "User doesn't exist !"
            return render(
                request,
                "authdemo/login.html",
                {
                    "error_message": error_message,
                    "body_class": "home",
                }
            )
        else:
            # The user exists and is fetched
            # Check if the provided password match the stored password
            if check_password(user_password, user.password):
                # The password is correct
                # Then update the session
                request.session.user = user
                request.session.save()
                # Proceed to next
                response = redirect(next_url) if next_url else redirect(reverse("authdemo:index"))
                # Update the cookie
                max_age = request.session.expiry.total_seconds()
                response.set_cookie("session_id", request.session.session_id, max_age=max_age)
                # Make the max-age accessible for further processing client-side
                response.set_cookie("maxAge", request.session.get_expiry_date)
                return response
            else:
                # The password is incorrect
                error_message["password"] = "Invalid password !"
                return render(
                    request,
                    "authdemo/login.html",
                    {
                        "error_message": error_message,
                        "body_class": "login",
                    }
                )
    else:
        # It is a GET request, simply render the login page
        return render(request, "authdemo/login.html", {"body_class": "login"})


def logout(request):
    """ Delete the corresponding session and cookies. """
    # Delete the session
    request.session.delete()
    # Optionally, expires the cookie
    response = redirect(reverse("authdemo:login"))
    response.delete_cookie("session_id")

    return response


class UserFormView(View):
    form_class = UserForm
    initial = {}
    template = "authdemo/register.html"

    # Request a form to create a new user
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, template_name=self.template, context={"form": form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("authdemo:login"), {"success": "User successfully created"})

        return render(request, self.template, context={"form": form})


@csrf_exempt
def file_upload(request):
    if request.method == "POST" and request.FILES.get("chunk"):
        try:
            # Extract request data
            chunk = request.FILES["chunk"].read()  # Read the chunk as raw bytes
            chunk_index = int(request.POST["chunkIndex"])
            total_chunks = int(request.POST["totalChunks"])
            file_name = request.POST["fileName"]
            file_extension = request.POST.get("fileExtension", "")

            user_id = request.session.user.user_id

            # Call Celery task asynchronously
            handle_file_upload_task.delay(
                file_name=file_name,
                file_extension=file_extension,
                chunk_data=chunk,
                chunk_index=chunk_index,
                total_chunks=total_chunks,
                user_id=user_id,
            )

            return HttpResponse("Chunk uploaded and queued for processing", status=202)

        except KeyError as e:
            return HttpResponse(f"Missing parameter: {str(e)}", status=400)

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return HttpResponse("No file uploaded", status=400)
