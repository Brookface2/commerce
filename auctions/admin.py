from django.contrib import admin

# Register your models here.
from .models import Listing, User, Bids, Comment

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Comment)