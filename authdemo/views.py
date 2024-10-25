from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.urls import reverse
from .models import User
from django.template import Template

# Create your views here.


def index(request):
    template = "authdemo/home.html"
    return render(request, template, context={"user": request.session.user, "request": request})


def login(request):

    next_url = request.GET.get("next")

    error_message = {}

    if request.method == "POST":
        user_firstname = request.POST.get("first-name")
        user_password = request.POST.get("password")

        try:
            # Fetching the user by its first name
            user = User.objects.get(first_name=user_firstname)
        except User.DoesNotExist:
            error_message["name"] = "User doesn't exist !"
            return render(
                request,
                "authdemo/login.html",
                {
                    "error_message": error_message
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
                        "error_message": error_message
                    }
                )
    else:
        # It is a GET request, simply render the login page
        return render(request, "authdemo/login.html")


def logout(request):
    """ Delete the corresponding session and cookies. """
    # Delete the session
    request.session.delete()
    # Optionally, expires the cookie
    response = redirect(reverse("authdemo:login"))
    response.delete_cookie("session_id")

    return response
