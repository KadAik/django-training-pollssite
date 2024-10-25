"""
Authentication middlewares
"""
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse


class AuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):

        # Check if the user is authenticated
        if not getattr(request.session, 'user', None):
            # If the user is not authenticated and the request is not for the login page
            if request.path != reverse('authdemo:login'):
                # Redirect to the login page with the next URL
                return HttpResponseRedirect(f"{reverse('authdemo:login')}?next={request.path}")

        response = self.get_response(request)

        return response
