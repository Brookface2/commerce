from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


# stores bids from users
class Bids(models.Model):
    bids_from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.current_bid}"
    
class Watchlist(models.Model):
    watchlist_user = models.ForeignKey(User, on_delete=models.CASCADE)
    on_watchlist = models.BooleanField()   

    def __str__(self):
        return f"{self.on_watchlist}"

#Stores listings
class Listing(models.Model):
    title = models.CharField(max_length=64)   
    description = models.CharField(max_length=256)
    category = models.CharField(max_length=256, blank=True)
    image = models.URLField()
    current_price = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="listing_bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listinguser")
    #comments = models.(Comment, on_delete=models.CASCADE, related_name="listing_comment", blank=True, null=True, to_field="comment")
    date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=datetime.now, null=True)
    on_watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name="watching_item", default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}-{self.id}"
    
#stores comments
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_comment")
    comment_for_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=256, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.comment}"
    
    class meta:
        ordering = ['date']
    
