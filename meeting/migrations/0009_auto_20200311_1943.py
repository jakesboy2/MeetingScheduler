# Generated by Django 3.0.2 on 2020-03-12 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0008_auto_20200305_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='date',
        ),
        migrations.AddField(
            model_name='meeting',
            name='end_date',
            field=models.DateField(default=0),
        ),
        migrations.AddField(
            model_name='meeting',
            name='start_date',
            field=models.DateField(default=0),
        ),
    ]
