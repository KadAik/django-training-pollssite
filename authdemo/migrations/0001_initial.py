# Generated by Django 5.1.1 on 2024-12-04 09:37

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('last_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'indexes': [models.Index(fields=['first_name', 'last_name'], name='authdemo_us_first_n_69440a_idx')],
                'constraints': [models.UniqueConstraint(fields=('first_name', 'last_name', 'email'), name='unique_full_name_email')],
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiry', models.DurationField(default=datetime.timedelta(seconds=1200))),
                ('container', models.JSONField(default=dict)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authdemo.user')),
            ],
        ),
        migrations.CreateModel(
            name='FileUploadTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255, unique=True)),
                ('chunk_count', models.IntegerField(default=0)),
                ('total_chunks', models.IntegerField()),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authdemo.user')),
            ],
        ),
    ]
