from django.forms import ModelForm
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "password"]
        error_messages = {
            "first_name": {
                "unique": "User already exists.",
                "required": "A user name is required"
            },

            "password": {
                "required": "A password is required",
            }
        }
