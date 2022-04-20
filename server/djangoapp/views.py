from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_dealers_from_cf, get_dealers_by_state, get_dealers_by_id, \
                      get_dealer_reviews_from_cf, \
                      add_dealer_review_to_cf
from .models import CarModel
import random
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def get_contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://ec95ec5f.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealership_list = get_dealers_from_cf(url)
        # Get dealers
        context = {
            'dealership_list':dealership_list
        }
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id=None):
    context = {}
    if request.method == "GET":
        url_review = "https://ec95ec5f.eu-gb.apigw.appdomain.cloud/api/review"
        url_dealer = "https://ec95ec5f.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealer_details_list = get_dealer_reviews_from_cf(url = url_review, dealerId = dealer_id)
        dealerships_info = get_dealers_by_id(url = url_dealer, dealerId = dealer_id)
        # Get dealers review
        context = {
            'dealerships_info':dealerships_info,
            'dealer_details_list':dealer_details_list,
        }
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id=None):
    context = {}
    url_dealer = "https://ec95ec5f.eu-gb.apigw.appdomain.cloud/api/dealership"
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        dealerships_info = get_dealers_by_id(url = url_dealer, dealerId = dealer_id)
        cars = CarModel.objects.all().filter(dealer_id = dealer_id)
        context = {
            "dealer_id": dealer_id,
            'dealerships_info': dealerships_info,
            "cars": cars,
        }
        return render(request, 'djangoapp/add_review.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user object
        user = request.user
        # Check Authentication
        if user.is_authenticated: 
            review ={}
            #review["id"] = dealer_id
            review["name"] = request.user.username
            review["review"] = request.POST['content']
            review["dealership"]= dealer_id

            if request.POST.get("purchasecheck") == 'on':
                car = CarModel.objects.get(pk=request.POST['car'])
                review["purchase"] = True
                review["purchase_date"]= datetime.strptime(request.POST['purchasedate'], "%m/%d/%Y").isoformat()
                review["car"] = car.car_name
                review["car_make"] = car.car_make.car_name
                review["car_year"] = car.car_year.strftime("%Y") 
            else:
                review["purchase"]= False
                
            json_payload = {
                "review": review
            } 

            url_post_review = "https://ec95ec5f.eu-gb.apigw.appdomain.cloud/api/dealership"
            post_request(url=url_post_review, json_payload = json_payload, dealerId=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            # Redirect to show_exam_result with the submission id
            return redirect('djangoapp:registration')