from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse
from .models import (User, InformationModel, EducationModel, SkillsModel, ExperienceModel, ProjectModel, MessageModel)

# Create your views here.
def index(request):

    return render(request, template_name="user_interface/index.html")


def login_view(request, *args, **kwargs):
    if request.method == "POST":
        # Prompt the user to sign in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Validate authentication
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "user_interface/loginRegister.html", {"message": "Wrong credentials!"})
        
    else:
            return render(request, "user_interface/loginRegister.html")
    


def logout_view(request):
     logout(request)

     return HttpResponseRedirect(reverse("index"))



def register_view(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # validating password
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "user_interface/loginRegister.html", {"message": "Passwords should match, Please try again!"})
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "user_interface/loginRegister.html", {"message": "Username already exists!"})
        
        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    else:
         return render(request, "user_interface/loginRegister.html")
        
        