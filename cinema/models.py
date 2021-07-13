from django.db import models


class Movie(models.Model):
    movie_name = models.CharField(max_length=250, blank=False)
    movie_genre = models.CharField(max_length=250, blank=False)
    movie_description = models.CharField(max_length=2000, blank=False)
    movie_price = models.IntegerField(default=0)
    movie_rating = models.DecimalField(default=0.0,decimal_places=1,max_digits=2)
    movie_photo = models.FileField(default=False)

    def __str__(self):
        return self.movie_name
