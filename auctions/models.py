from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    comment_for_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.CharField(max_length=256, blank=True)
    date = models.DateField(auto_now=True)

class Bids(models.Model):
    bids_from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.current_bid}"
    
    class meta:
        ordering = ['current_bid']


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.CharField(max_length=256, blank=True)
    image = models.URLField()
    current_price = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="listing_bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listinguser")
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="listing_comment", blank=True, null=True)


    def __str__(self):
        return f"{self.title}-{self.id}"
    
# class Bids(models.Model):
#     bids_from_user = models.ForeignKey(User, on_delete=models.CASCADE)
#     current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     date = models.DateField(auto_now=True)
#     bid_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bid")

#     def __str__(self):
#         return f"{self.current_bid}-{self.id}"

    

