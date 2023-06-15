""" RUN python3 manage.py makemigrations AND python3 manage.py migrate FOR NEW CHANGES"""

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listings(models.Model):
    """ id auto--> listing.id """
    lister = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="poster")
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    image_url = models.URLField()
    category = models.CharField(max_length=150)
    time = models.DateTimeField(auto_now_add=True)
    open = models.BooleanField(default=True)
    winner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, default=1, related_name="bidder")

    def __str__(self):
        return f"{self.id}"



class Bids(models.Model):
    listing =  models.ForeignKey(Listings, default=0, blank=True, on_delete=models.CASCADE)
    bid_value = models.FloatField()
    bidder = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add = True)

class Comments(models.Model):
    listing = models.ForeignKey(Listings, default=0, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, default=0, on_delete=models.CASCADE)
    comment = models.TextField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, blank=True, default=0, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, default=0, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id}"
