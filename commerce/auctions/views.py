from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.forms import TextInput
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Category, Bid, Comment

class CreateForm(forms.Form):
    title = forms.CharField(widget=TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    starting_bid = forms.DecimalField(widget=TextInput(attrs={'placeholder': 'Starting Bid'}), min_value=0, max_digits=10, decimal_places=2)
    image_url = forms.URLField(widget=TextInput(attrs={'placeholder': 'Image URL'}), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")
  
    

# Active listings
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True),
        "headline": "Active Listings"
    })


# Active and closed listings
def all(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "headline": "All Listings"
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            creator = request.user
            listing = Listing(title=title, description=description, starting_bid=starting_bid, current_bid=starting_bid, image_url=image_url, category=category, creator=creator)
            listing.save()
            return HttpResponseRedirect(reverse("index")) 
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
        form = CreateForm()
        return render(request, "auctions/create.html", {
            "form": form
        })


def my_listings(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(creator=request.user),
        "headline": "My Listings"
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
    })
    

def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        action = request.POST.get("action")
        listing = Listing.objects.get(pk=listing_id)
        # Check if the listing is already in the user's watchlist
        if action == "add":
            # Add the listing to the user's watchlist
            request.user.watchlist.add(listing)
            request.user.save()
            message = "Added to watchlist"
        elif action == "remove":
            # Remove the listing from the user's watchlist
            request.user.watchlist.remove(listing)
            request.user.save()
            message = "Removed from watchlist"
        else:
            message = "Error"
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "message": message
    })
    else:
        try:
            listings = request.user.watchlist.all()
        except:
            listings = []
        return render(request, "auctions/index.html", {
            "listings": listings,
            "headline": "My Watchlist"
        })
    






@login_required(login_url='/login')
def bid(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        bid = float(request.POST.get("bid"))
        listing = Listing.objects.get(pk=listing_id)
        if float(bid) > listing.current_bid:
            listing.current_bid = float(bid)
            listing.winner = request.user
            listing.save()
            request.user.bids.add(listing)
            request.user.save()
            bid = Bid(user=request.user, listing=listing, amount=bid)
            bid.save()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Bid placed"
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Bid must be higher than current bid"
            })
    else:
        return HttpResponseRedirect(reverse("index"))


def my_bids(request):
    bids = request.user.bids.all()
    return render(request, "auctions/index.html", {
        "listings": bids,
        "headline": "My Bids"
    })


def close(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Listing closed"
        })
    else:
        return HttpResponseRedirect(reverse("index"))
    


def category(request, category_name):
    category = Category.objects.get(name=category_name)
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category),
        "headline": category_name
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


@login_required(login_url='/login')
def comment(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        listing = Listing.objects.get(pk=listing_id)
        comment = request.POST.get("comment")
        comment = Comment(user=request.user, listing=listing, comment=comment)
        comment.save()
        return redirect("listing", listing_id=listing_id)