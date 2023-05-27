from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse
from .models import (User, InformationModel, EducationModel, SkillsModel, ExperienceModel, ProjectModel, MessageModel)
from .forms import (IntroForm, EducationForm, SkillsForm, ExperienceForm, ProjectForm, MessageForm, ContactForm)
import logging

logger = logging.Logger("logger")
logger.setLevel("INFO")

# Create your views here.
def index(request):

    return render(request, template_name="user_interface/index.html")



def form_createView(request, *args, **kwargs):
    template_name = "user_interface/create.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"
    # intro form
    info_form = IntroForm(request.POST or None)
    if info_form.is_valid():
        info_form.save(commit=False)
        info_form.user = user
        info_form.save()
    else:
        info_form = IntroForm()

    # education form
    edu_form = EducationForm(request.POST or None)
    if edu_form.is_valid():
        edu_form.save(commit=False)
        edu_form.user = user
        edu_form.save()
    else:
        edu_form = EducationForm()

    # skills form
    skills_form = SkillsForm(request.POST or None)
    if skills_form.is_valid():
        skills_form.save(commit=False)
        skills_form.user = user
        skills_form.save()
    else:
        skills_form = SkillsForm()

    # experience form
    exp_form = ExperienceForm(request.POST or None)
    if exp_form.is_valid():
        exp_form.save(commit=False)
        exp_form.user = user
        exp_form.save()
    else:
        exp_form = ExperienceForm()

    # project form
    project_form = ProjectForm(request.POST or None)
    if project_form.is_valid():
        project_form.save(commit=False)
        project_form.user = user
        project_form.save()
    else:
        project_form = ProjectForm()

    context = {
        'introFORM': info_form,
        'eduFORM': edu_form,
        'expFORM': exp_form,
        'projectFORM': project_form,
        'skillsFORM': skills_form

    }

    return render(request, template_name, context)



def login_view(request, *args, **kwargs):
    if request.method == "POST":
        # Prompt the user to sign in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        logger.info(f"User '{user}' attempting to log in")

        # Validate authentication
        if user is not None:
            logger.info("User not found...")
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            logger.info("Wrong login credentials")
            return render(request, "user_interface/loginRegister.html", {"message": "Wrong credentials!"})
        
    else:
        logger.info("Logging in attempted with a different method...")    
        return render(request, "user_interface/loginRegister.html")
    


def logout_view(request):
     logout(request)

     return HttpResponseRedirect(reverse("index"))



def register_view(request, *args, **kwargs):
    if request.method == "POST":
        logger.info("Registering new user...")
        username = request.POST["username"]
        email = request.POST["email"]

        # validating password
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            logger.info("User passwords do not match...")
            return render(request, "user_interface/loginRegister.html", {"message": "Passwords should match, Please try again!"})
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            logger.info(f"User '{user}' added...")
        except IntegrityError:
            logger.info(f"User '{user}' already in the system")
            return render(request, "user_interface/loginRegister.html", {"message": "Username already exists!"})
        
        logger.info(f"Logging in {user}")
        login(request, user)
        

        return HttpResponseRedirect(reverse("index"))
    else:
         logger.info("Wrong register method used...")
         return render(request, "user_interface/loginRegister.html")
        
        