# Generated by Django 3.2.4 on 2021-09-15 16:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0004_alter_movie_movie_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_day',
            field=models.CharField(default='Monday', max_length=200),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_num_of_tickets',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]