from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid", views.bid, name="bid"),
    path("my_bids", views.my_bids, name="my_bids"),
    path("close", views.close, name="close"),
    path("listing/all", views.all, name="all"),
    path("category/<str:category_name>", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("comment", views.comment, name="comment")
]
