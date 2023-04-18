from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import datetime
from dateutil.parser import parse


from .models import User, Listing, Bids, Comment, Watchlist

class Bid_form(forms.Form):
    bid = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'name':'Bid'}))

class Create_listing(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'name':'Title'}))
    description = forms.CharField(max_length=64, widget=forms.Textarea(attrs={'name':'Descriptions', 'rows':3, 'columns':4}))
    start_bid = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'name':'Starting Bid'}))
    url = forms.URLField(label='URL')
    category = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'name':'Category'}))
    end_date = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget , label='End Date')

class Comment_form(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'name':'Comment', 'rows':2, 'columns':4}), max_length=256)

def index(request):
        message = "No Active Listings!"
        items = Listing.objects.filter()
        for item in items:
            if datetime.now().timestamp() < parse(str(item.end_date)).timestamp():
                item.active = False
                return render(request, "auctions/index.html",{
                    'listings':Listing.objects.filter(active=True),
                    'message':message
                })
            else:
                return render(request, "auctions/index.html", {
                    'message':message
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
    
    #creates a new listing
def create(request):
    if request.method == "GET":
        return render(request, "auctions/createlisting.html",{
            'form': Create_listing(initial={"end_date":datetime.now})
        })
    elif request.method == "POST":
        form = Create_listing(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            current_bid = form.cleaned_data["start_bid"]
            link = form.cleaned_data["url"]
            category = form.cleaned_data["category"]
            end_date = form.cleaned_data["end_date"]
            item_bid = Bids(current_bid=current_bid, bids_from_user=request.user)
            item_bid.save()
            item_watchlist = Watchlist(watchlist_user=request.user, on_watchlist=False)
            item_watchlist.save()
            listing = Listing(title = title, current_price=item_bid, description = description, category = category, image = link, user=request.user, end_date=end_date, on_watchlist=item_watchlist)
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            message = "Form is not valid!"
            return render(request, "auctions/createlisting.html",{
                'message':message,
                'form':Create_listing(request.POST)
            })
    else:
        return render(request, "auctions/createlisting.html")
    

# gets the listing with it's ID
def listing(request, listing_id):
    requested = Listing.objects.get(pk=listing_id)
    if request.method == "GET":
        return render(request, "auctions/listing.html",{
            'page':requested,
            'bid_form':Bid_form(),
            'comment_form':Comment_form(),
            'listing_comments':Comment.objects.filter(listing=listing_id).order_by('-date')
        })
    # if method is post - updates the bid
    elif request.method == "POST" and "bid" in request.POST:
        form = Bid_form(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            # gets current bid ID
            current_bid_id = requested.current_price.id
            # compares current bid against new bid 
            if requested.current_price.current_bid < bid:
                # creates new bid instance with current bid ID
                test = Bids.objects.get(id=current_bid_id)
                # assigns new bid to the curent bid
                test.current_bid = bid
                test.bids_from_user = request.user
                # saves new bid 
                test.save()
                return HttpResponseRedirect(reverse("listing", args=(requested.id,)))
            else:
                # if bid is lower than current bid message is printed to tell user
                message = f"Your bid is less than current bid"
                return render(request, "auctions/listing.html",{
                    'title':requested,
                    'page':requested,
                    'bid_form':Bid_form(),
                    'comment_form':Comment_form(),
                    'message':message,
                    'listing_comments':Comment.objects.filter(listing=listing_id).order_by('-date')
                })
    elif request.method == "POST" and "comment" in request.POST:
        listing=Listing.objects.get(pk=listing_id)
        listing_comment = Comment.objects.filter(listing=listing_id)
        comment = Comment_form(request.POST)
        if comment.is_valid():
            new_comment = comment.cleaned_data['comment']
            save_comment = Comment(comment_for_user=request.user, comment=new_comment, listing=listing)
            save_comment.save()
            return render(request, "auctions/listing.html",{
            'title':requested,
            'page':requested,
            'bid_form':Bid_form(),
            'comment_form':Comment_form(),
            'listing_comments':Comment.objects.filter(listing=listing_id)
            })
            # else:
            #      return HttpResponseRedirect(reverse("listing", args=(requested.id,)))
        else:
                return HttpResponseRedirect(reverse("listing", args=(requested.id,)))
    else:
        return HttpResponseRedirect(reverse("listing", args=(requested.id,)))

def watchlisted(request):
    if request.method == "POST" and "watchlist" in request.POST:
        watchlist=Listing.objects.get(pk=request.id)
        watchlist.on_watchlist = True
        watchlist.save()
    listing = Listing.objects.filter()
    return render(request, "auctions/watchlist.html",{
        'on_watchlist':listing,
    })