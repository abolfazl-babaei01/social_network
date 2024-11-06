# Generated by Django 5.1 on 2024-11-01 21:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_rename_user_form_contact_user_from'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_message_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_message_form_set', to=settings.AUTH_USER_MODEL)),
                ('user_message_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_message_to_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='socialuser',
            name='message',
            field=models.ManyToManyField(related_name='messages', through='account.Message', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['-created'], name='account_mes_created_e923e5_idx'),
        ),
    ]
