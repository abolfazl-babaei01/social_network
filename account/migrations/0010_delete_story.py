# Generated by Django 5.1 on 2024-11-08 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_story'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Story',
        ),
    ]