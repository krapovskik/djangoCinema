from django.db import models
import datetime


class Movie(models.Model):
    movie_name = models.CharField(max_length=250, blank=False)
    movie_genre = models.CharField(max_length=250, blank=False)
    movie_description = models.CharField(max_length=2000, blank=False)
    movie_price = models.IntegerField(default=0,blank=True)
    movie_rating = models.DecimalField(default=0.0,decimal_places=1,max_digits=2,blank=True)
    movie_photo = models.FileField(default=False, blank=False)
    movie_num_of_tickets = models.IntegerField(default=0, blank=True)
    movie_time = models.TimeField(default=datetime.time(0, 0), blank=True)
    movie_day = models.CharField(default='Monday', max_length=200, blank=True)
    movie_comming_soon = models.BooleanField(default=False)


    def __str__(self):
        return self.movie_name
