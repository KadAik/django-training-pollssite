This app intents to implements a *session-cookie* based authentication.

In a session-cookie based authentication, when a user in authenticated,
a session is created for this user and a session_id is set on the cookie.
For further request, the server checks if a cookie contains a session_id
key. If it does, the server fecth the associated user and process the
request further. If it doesn't, the user is required to autenticate.

The logout process is accomplished by either expire the cookie or and 
foremost delete the session in the database.

# Implementation with django

Django automatically handles session when a project is initilized. It handles it
via the `django.contrib.session.SessionMiddleware` session.

To use our own system,
- Remove `django.contrib.session.SessionMiddleware` in MIDDLEWARE
    from settings.py
- From INSTALLED8APPS, remove django.contrib.sessions
- Comment out admin urls in the project urls file and unregister (comment)
    django.contrib.admin to prevent errors as using admin require 
    SessionMiddleware to be installed.
- Also comment `django.contrib.auth.middleware.AuthenticationMiddleware` and
    `django.contrib.messages.middleware.MessageMiddleware`.
    Those depend on each other and require SessionMiddleware.
