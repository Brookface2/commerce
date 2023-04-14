from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bids, Comment

class Bid_form(forms.Form):
    bid = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput)



def index(request):
        return render(request, "auctions/index.html",{
            'listings':Listing.objects.filter()
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
    
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        current_bid = request.POST["bid"]
        link = request.POST["URL"]
        category = request.POST["category"]
        item_bid = Bids(current_bid=current_bid, bids_from_user=request.user)
        item_bid.save()
        listing = Listing(title = title, current_price=item_bid, description = description, category = category, image = link, user=request.user)
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        return render(request, "auctions/createlisting.html")
    
def listing(request, listing_id):
    requested = Listing.objects.get(pk=listing_id)
    if request.method == "GET":
        return render(request, "auctions/listing.html",{
            'page':requested,
            'form':Bid_form()
        })
    elif request.method == "POST":
        form = Bid_form(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            new_bid = Bids(current_bid=bid, bids_from_user=request.user)
            if requested.current_price.current_bid < new_bid.current_bid:
                Bids.objects.update(current_bid=bid)
                message = f"Bid Accepted!"
                return HttpResponseRedirect(reverse("listing", args=(requested.id,)),{
                    'title':requested,
                    'page':requested,
                    'form':Bid_form(),
                    'message':message,
                })
            else:
                message = f"Your bid is less than current bid"
                return render(request, "auctions/listing.html",{
                    'title':requested,
                    'page':requested,
                    'form':Bid_form(request.POST),
                    'message':message
                })
        else:
            bid = request.POST["bid"]
            message=f" {bid} dont do no bids"
            return render(request, "auctions/listing.html",{
            'title':requested,
            'page':requested,
            'form':Bid_form(),
            'message':message
        })
