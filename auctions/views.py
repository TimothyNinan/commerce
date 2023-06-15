from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listings, Bids, Comments, Watchlist
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

def index(request):
    listings = Listings.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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

@login_required
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

@login_required
def create_listing(request):
    if (request.method == "POST"):
        results = request.POST
        listing = Listings(lister=request.user ,title=results['title'], description=results['description'], price=results['start_bid'], image_url=results['image_url'], category=results['category'], open=True)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else: 
        return render(request, "auctions/list.html", {})

def view_listing(request, listing_name):
    
    if (request.method == "POST"):
        results = request.POST
        try:
            listing = Listings.objects.get(title=listing_name)
        except Listings.DoesNotExist:
            listing = None
            return render(request, "auctions/error.html", {
                'message': "Listing Does Not Exist. Try Again or Create this Listing."
            })
        try:
            watchs = results['watchlist']
        except MultiValueDictKeyError:
            watchs = "No"
        try:
            bidd = results['bid']
        except MultiValueDictKeyError:
            bidd = "No"
        try:
            comm = results['comment']
        except MultiValueDictKeyError:
            comm = "No"
        try:
            closse = results['close']
        except MultiValueDictKeyError:
            closse = "No"
        if (watchs == "Add to Watchlist"):
            watchlist_item = Watchlist(user=request.user, listing=listing)
            watchlist_item.save()
            return HttpResponseRedirect(f"/{listing_name}")
        elif (watchs == "Remove from Watchlist"):
            watchlist_item = Watchlist.objects.get(user=request.user, listing=listing)
            watchlist_item.delete()
            return HttpResponseRedirect(f"/{listing_name}")
        if (closse == "Close Listing"):
            if (listing.lister == request.user):
                listing.open = False
                winning_price = listing.price
                try:
                    winning_bid =  Bids.objects.get(bid_value=winning_price)
                    winner_name = winning_bid.bidder
                    winning_user = User.objects.get(username=winner_name)
                    listing.winner = winning_user
                    listing.winner = winning_user
                    listing.save()
                except Bids.DoesNotExist:
                    listing.save()
                return HttpResponseRedirect(f"/{listing_name}")
            else:
                return render(request, "auctions/error.html", {
                    'message': "You do not have permission to close this listing."
                })
        if (comm == "Submit Comment"):
            comment_item = Comments(listing=listing, user=request.user, comment=results['new_comment'])
            comment_item.save()
            return HttpResponseRedirect(f"/{listing_name}")
        if (bidd == "Place Bid"):
            current_price = listing.price
            bid = results["new_bid"]
            if (int(bid) > current_price):
                new_bid = Bids(listing=listing, bid_value=bid, bidder=request.user)
                new_bid.save()
                listing.price = bid
                listing.save()
                return HttpResponseRedirect(f"/{listing_name}")
            else:
                return render(request, "auctions/error.html", {
                    'message': "New Bid must be Higher than Current Price"
                })
    else:
        try:
            listing = Listings.objects.get(title=listing_name)
        except Listings.DoesNotExist:
            listing = None
            return render(request, "auctions/error.html", {
                'message': "Listing Does Not Exist. Try Again or Create this Listing."
            })
        try:
            comments = Comments.objects.filter(listing=listing)
        except Comments.DoesNotExist:
            comments = "No Comments"
        if request.user.is_authenticated:
            try:
                watchlist_item = Watchlist.objects.get(user=request.user, listing=listing)
            except Watchlist.DoesNotExist:
                watchlist_item = ""
            if (watchlist_item == ""):
                is_watchlist = False
            else:
                is_watchlist = True
            return render(request, "auctions/view.html", {
                'list': listing,
                'watchlist': is_watchlist,
                'comments': comments
            })
        else:
           return render(request, "auctions/view.html", {
                'list': listing,
                'comments': comments
            }) 

def category(request):
    if (request.method == "POST"):
        results = request.POST
        cat = results['category']
        listings = Listings.objects.filter(category=cat)
        return render(request, "auctions/category.html", {
            'listings': listings
        })
    else:
        return render(request, "auctions/category.html", {
            'listings': None
        })

@login_required
def watchlist(request):
    listings = []
    watchlists = Watchlist.objects.filter(user=request.user)
    for watchlist in watchlists:
        list = Listings.objects.get(pk=watchlist.listing.id)
        listings.append(list)
    return render(request, "auctions/watchlist.html", {
        'listings': listings
    })