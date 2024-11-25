import time

from django.db import models, transaction
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db.models import F
import datetime
from django.db.utils import OperationalError

# Create your models here.


class User(models.Model):

    user_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, unique=True)
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

    container = models.JSONField(default=dict)

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

    def __getitem__(self, item):
        return self.container.get(item, None)

    def __setitem__(self, key, value):
        self.container[key] = value
        self.save()


class FileUploadTracker(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    file_name = models.CharField(max_length=255, unique=True)
    chunk_count = models.IntegerField(default=0)
    total_chunks = models.IntegerField()
    upload_time = models.DateTimeField(auto_now_add=True)

    def update_chunk_count(self, max_retries=5, delay=0.5):
            """
            Update the chunk count atomically and handle database locks with retries.
            Args:
                max_retries (int): Maximum number of retry attempts.
                delay (float): Delay between retries in seconds.
            Raises:
                OperationalError: If the database remains locked after max retries.
            """
            for attempt in range(max_retries):
                try:
                    with transaction.atomic():
                        # Lock the record and increment the chunk count
                        file_tracked = FileUploadTracker.objects.select_for_update().get(id=self.id)
                        file_tracked.chunk_count += 1
                        file_tracked.save()
                    return  # Exit if successful
                except OperationalError as op_error:
                    if "database is locked" in str(op_error):
                        time.sleep(delay)  # Wait before retrying
                    else:
                        raise  # Re-raise any other database error
            # If all retries fail, raise an error
            raise OperationalError("Failed to update chunk count after multiple retries due to database lock.")

    def __str__(self):
        return f"File: {self.file_name}, User: {self.user.first_name}, Total chunks: {self.total_chunks}"



