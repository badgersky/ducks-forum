# Generated by Django 4.2.1 on 2023-05-14 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ducks', '0003_duck_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='duck',
            name='avg_height',
        ),
    ]
