# Generated by Django 2.2.7 on 2020-02-06 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("EloMain", "0015_remove_club_logo"),
    ]

    operations = [
        migrations.RemoveField(model_name="championship", name="icon",),
    ]
