# Generated by Django 5.0.7 on 2024-08-03 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='answers_count',
        ),
    ]
