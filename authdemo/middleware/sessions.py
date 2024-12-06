"""
Manage sessions
"""
from authdemo.models import Session
from django.http import HttpRequest
from django.db.models import F
from datetime import timedelta


class SessionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        """Attach a session object to an incoming request."""

        session_id = request.COOKIES.get("session_id", False)
        if session_id:
            try:
                # If the session exists, is it valid ?
                session = Session.objects.get(session_id=session_id)
                if session.invalidate():
                    session = Session()
                else:
                    # Reset the timer for expiration
                    # session.expiry = F("sessions") + timedelta(minutes=5)
                    pass
            except Session.DoesNotExist:
                # The session doesn't exist; initialize a session
                session = Session()
                # Persist the session
                session.save()
        else:
            session = Session()
            session.save()

        # Attach a session object to the incoming request
        request.session = session
        # Proceed to next
        response = self.get_response(request)

        return response



