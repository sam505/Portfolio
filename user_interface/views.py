from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import (User, InformationModel, EducationModel, SkillsModel, ExperienceModel, ProjectModel, MessageModel)
from .forms import (IntroForm, EducationForm, SkillsForm, ExperienceForm, ProjectForm, MessageForm, ContactForm)
import logging
from .serializers import (userSerializer, informationSerializer, educationSerializer, experienceSerializer, projectSerializer, skillsetSerializer, messageSerializer)
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import serializers, permissions


logger = logging.Logger("logger")
logger.setLevel("INFO")

# Create your views here.
def index(request):

    return render(request, template_name="user_interface/index.html")


@login_required(login_url="login")
def form_create_view(request, *args, **kwargs):
    template_name = "user_interface/information.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    # intro form
    info_form = IntroForm(request.POST or None)
    if info_form.is_valid():
        info_form.save(commit=False)
        info_form.user = user
        info_form.save(request=request)
        return HttpResponseRedirect(reverse('education'))
    else:
        info_form = IntroForm()

    context = {
        'user': user,
        'introFORM': IntroForm(),
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def form_create_education_view(request, *args, **kwargs):
    template_name = "user_interface/education.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    # education form
    edu_form = EducationForm(request.POST or None)
    if edu_form.is_valid():
        edu_form.save(commit=False)
        edu_form.user = user
        edu_form.save(request=request)
        return HttpResponseRedirect(reverse('experience'))
    else:
        edu_form = EducationForm()

    context = {
        'user': user,
        'eduFORM': EducationForm(),
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def form_create_experience_view(request, *args, **kwargs):
    template_name = "user_interface/experience.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    # experience form
    exp_form = ExperienceForm(request.POST or None)
    if exp_form.is_valid():
        exp_form.save(commit=False)
        exp_form.user = user
        exp_form.save(request=request)
        return HttpResponseRedirect(reverse('project'))
    else:
        exp_form = ExperienceForm()


    context = {
        'user': user,
        'expFORM': ExperienceForm(),
    }

    return render(request, template_name, context)



@login_required(login_url="login")
def form_create_project_view(request, *args, **kwargs):
    template_name = "user_interface/project.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    # project form
    project_form = ProjectForm(request.POST or None)
    if project_form.is_valid():
        project_form.save(commit=False)
        project_form.user = user
        project_form.save(request=request)
        return HttpResponseRedirect(reverse('skillset'))
    else:
        project_form = ProjectForm()

    context = {
        'user': user,
        'projectFORM': ProjectForm(),
    }

    return render(request, template_name, context)



@login_required(login_url="login")
def form_create_skillset_view(request, *args, **kwargs):
    template_name = "user_interface/skillset.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    # skills form
    skills_form = SkillsForm(request.POST or None)
    if skills_form.is_valid():
        skills_form.save(commit=False)
        skills_form.user = user
        skills_form.save(request=request)
    else:
        skills_form = SkillsForm()


    context = {
        'user': user,
        'skillsFORM': SkillsForm(),
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
            return HttpResponseRedirect(reverse("create"))
        
        else:
            logger.info("Wrong login credentials")
            return render(request, "user_interface/loginRegister.html", {"message": "Wrong credentials!"})
        
    else:
        logger.info("Logging in attempted with a different method...")    
        return render(request, "user_interface/loginRegister.html")
    


def logout_view(request):
     logout(request)

     return HttpResponseRedirect(reverse("login"))



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
        

        return HttpResponseRedirect(reverse("login"))
    else:
         logger.info("Wrong register method used...")
         return render(request, "user_interface/loginRegister.html")


def get_user_data(username):
    bioProfile = User.objects.get(username=username)
    information_qs = InformationModel.objects.filter(user=bioProfile).first()
    education_qs = EducationModel.objects.filter(user=bioProfile).all()
    experience_qs = ExperienceModel.objects.filter(user=bioProfile).all()
    project_qs = ProjectModel.objects.filter(user=bioProfile).all()
    skillset_qs = SkillsModel.objects.filter(user=bioProfile).all()
    message_qs = MessageModel.objects.filter(user=bioProfile).all()
    messageform_qs = MessageForm()

    # initialize serializers
    username_api = userSerializer(bioProfile, many=False)
    information_api = informationSerializer(information_qs, many=False)
    education_api = educationSerializer(education_qs, many=True)
    experience_api = experienceSerializer(experience_qs, many=True)
    project_api = projectSerializer(project_qs, many=True)
    skillset_api = skillsetSerializer(skillset_qs, many=True)
    message_api = messageSerializer(message_qs, many=True)

    context = {
        "username": username,
        "user": username_api.data,
        "information": information_api.data,
        "education": education_api.data,
        "experience": experience_api.data,
        "projects": project_api.data,
        "skillsets": skillset_api.data,
        "message_form": message_api.data

    }

    return context
        
        
@api_view(["GET"])
@permission_classes((permissions.AllowAny, permissions.IsAuthenticated))
def api_view(request, username, *args, **kwargs):
    context = get_user_data(username)

    return Response(context)


def portfolio_view(request, username, *args, **kwargs):
    template_name = "user_interface/portfolio.html"
    # method 1
    # try:
    #     userprofile = User.objects.get(username=username)
    # except User.DoesNotExist:
    #     raise Http404("User does not exist")

    # method 2
    user_profile = get_object_or_404(User, username=username)
    if request.method == "GET":
        context = get_user_data(username)

    return render(request, template_name, context)
