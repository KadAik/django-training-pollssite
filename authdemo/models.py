from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db.models import F
import datetime
# Create your models here.


class User(models.Model):

    user_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    # Amending the save method to hash the password field before storing it in the db
    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.password.startswith('pbkdf2_'):  # Prevent double hashing
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DurationField(default=datetime.timedelta(minutes=20))

    def __str__(self):
        return str(self.session_id)

    def invalidate(self):
        """
        Delete the session if it expires and return True if deletion successful
        """
        # Calculate the expiration time
        print(f"Created at: {self.created_at}")
        print(f"Will expire at: {self.expiry}")

        expiration_time = self.created_at + self.expiry

        if timezone.now() >= expiration_time:
            self.delete()
            return True
        return False

    @property
    def get_expiry_date(self):
        return self.created_at + self.expiry
