from django.contrib import admin
from .models import User, Listing, Category, Bid

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "starting_bid", "current_bid", "category", "image_url", "creator", "created_date", "active", "watchlist", "bidder")
    

class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "amount", "timestamp")


# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Bid)