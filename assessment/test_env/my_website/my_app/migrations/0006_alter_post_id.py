# Generated by Django 4.2.4 on 2024-03-22 11:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0005_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
