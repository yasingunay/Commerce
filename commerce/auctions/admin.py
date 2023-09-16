from django.contrib import admin
from .models import User, Listing, Category, Bid, Comment

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "starting_bid", "current_bid", "category", "image_url", "creator", "created_date", "active", "watchlist", "bidder")
    

class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "amount", "timestamp")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "comment", "timestamp")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)