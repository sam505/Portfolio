from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from .models import (User, InformationModel, EducationModel,
                     SkillsModel, ExperienceModel, ProjectModel, MessageModel)
from .forms import (IntroForm, EducationForm, SkillsForm,
                    ExperienceForm, ProjectForm, MessageForm, ContactForm)
import logging as logger
from .serializers import (userSerializer, informationSerializer, educationSerializer,
                          experienceSerializer, projectSerializer, skillsetSerializer, messageSerializer)
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import serializers, permissions
from django.template.loader import render_to_string

logger.basicConfig(
    level=logger.INFO, 
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s'
                   )

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
    info_form = IntroForm(request.POST, request.FILES)
    if info_form.is_valid():
        info_form.save(commit=False)
        info_form.user = user
        info_form.save(request=request)

        return redirect('education')
        
    else:
        if request.method == "GET":
            context = {
            'user': user,
            'introFORM': IntroForm(),
        }
        else:
            context = {
                'user': user,
                'introFORM': info_form,
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
    edu_form = EducationForm(request.POST)
    if edu_form.is_valid():
        edu_form.save(commit=False)
        edu_form.user = user
        edu_form.save(request=request)

        return redirect('experience')
    
    else:
        if request.method == "GET":
            context = {
            'user': user,
            'eduFORM': EducationForm(),
        }
        else:
            context = {
                'user': user,
                'eduFORM': edu_form,
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
    exp_form = ExperienceForm(request.POST)
    if exp_form.is_valid():
        exp_form.save(commit=False)
        exp_form.user = user
        exp_form.save(request=request)

        return redirect('project')
    
    else:
        if request.method == "GET":
            context = {
                'user': user,
                'expFORM': ExperienceForm(),
            }

        else:
            context = {
                    'user': user,
                    'expFORM': exp_form,
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
    project_form = ProjectForm(request.POST, request.FILES)
    if project_form.is_valid():
        project_form.save(commit=False)
        project_form.user = user
        project_form.save(request=request)

        return redirect('skillset')
    
    else:
        if request.method == "GET":
            context = {
            'user': user,
            'projectFORM': ProjectForm(),
        }
        else:
            context = {
                'user': user,
                'projectFORM': project_form,
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
    skills_form = SkillsForm(request.POST, request.FILES)
    if skills_form.is_valid():
        skills_form.save(commit=False)
        skills_form.user = user
        skills_form.save(request=request)

        return redirect('portfolio', user.username)

    else:
        if request.method == "GET":
            context = {
                'user': user,
                'skillsFORM': SkillsForm(),
            }
        else:
            context = {
                'user': user,
                'skillsFORM': skills_form,
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
            return HttpResponseRedirect(reverse("information"))

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
    logger.info(f"Getting data for {username}...")
    bioProfile = User.objects.filter(username=username).first()
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
        # "message_form": message_api.data

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
    context = get_user_data(username)
    user_profile = get_object_or_404(User, username=username)
    context = get_user_data(username)
    if request.method == "GET":
        form = ContactForm()
        context["form"] = form
    else:
        to_email = context["information"]["userEmail"]
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            from_email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            phone = form.cleaned_data["phone"]
            message = form.cleaned_data['message']

            try:
                msg_html = render_to_string('user_interface/email.html', {'name': name,
                                                                          'from': from_email,
                                                                          'subject': subject,
                                                                          'phone': phone,
                                                                          'message': message,
                                                                          'username': username
                                                                          })

                send_mail(
                    subject,
                    message,
                    from_email,
                    [to_email],
                    html_message=msg_html,
                )
                logger.info("Mail sent successfully...")
            except Exception as e:
                logger.error("Sending mail failed...")
                return HttpResponse(f"Bad/Invalid Header found {e}")
        context["form"] = form
    return render(request, template_name, context)


# ------------------------------ UPDATE -------------------------------
@login_required(login_url="login")
def form_update_view(request, *args, **kwargs):
    template_name = "user_interface/update/information.html"
    context = {}
    user = request.user
    logger.info("Updating Introduction Form...")
    if not user.is_authenticated:
        user = "admin"

    try:
        obj = InformationModel.objects.filter(user=user).first()
    except:
        raise Http404

    # intro form
    info_form = IntroForm(request.POST, request.FILES, instance=obj)
    if info_form.is_valid():
        info_form.save(commit=False)
        info_form.user = user
        info_form.save(request=request)
        logger.info("Introduction form updated...")
    else:
        logger.error(f"{request.method} Introduction form is Invalid...")
        if request.method == "GET":
            info_form = IntroForm(instance=obj)

    context = {
        'user': user,
        'introFORM': info_form,
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def form_update_education_view(request, *args, **kwargs):
    template_name = "user_interface/update/education.html"
    context = {}
    logger.info("Updating Education form...")
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    try:
        obj = EducationModel.objects.filter(user=user).first()
    except:
        raise Http404

    # education form
    edu_form = EducationForm(request.POST, instance=obj)
    if edu_form.is_valid():
        logger.info("Valid Education form...")
        edu_form.save(commit=False)
        edu_form.user = user
        edu_form.save(request=request)
    else:
        logger.info("Valid Education form...")
        if request.method == "GET":
            edu_form = EducationForm(instance=obj)

    context = {
        'user': user,
        'eduFORM': edu_form,
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def form_update_experience_view(request, *args, **kwargs):
    template_name = "user_interface/update/experience.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    try:
        obj = ExperienceModel.objects.filter(user=user).first()
    except:
        raise Http404

    # experience form
    exp_form = ExperienceForm(request.POST, instance=obj)
    if exp_form.is_valid():
        exp_form.save(commit=False)
        exp_form.user = user
        exp_form.save(request=request)
    else:
        if request.method == "GET":
            exp_form = ExperienceForm(instance=obj)

    context = {
        'user': user,
        'expFORM': exp_form,
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def form_update_project_view(request, *args, **kwargs):
    template_name = "user_interface/update/project.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    try:
        obj = ProjectModel.objects.filter(user=user).first()
    except:
        raise Http404

    # project form
    project_form = ProjectForm(request.POST, request.FILES, instance=obj)
    if project_form.is_valid():
        project_form.save(commit=False)
        project_form.user = user
        project_form.save(request=request)
    else:
        if request.method == "GET":
            project_form = ProjectForm(instance=obj)

    context = {
        'user': user,
        'projectFORM': project_form,
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def form_update_skillset_view(request, *args, **kwargs):
    template_name = "user_interface/update/skillset.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    try:
        obj = SkillsModel.objects.filter(user=user).first()
    except:
        raise Http404

    # skills form
    skills_form = SkillsForm(request.POST, request.FILES, instance=obj)
    if skills_form.is_valid():
        skills_form.save(commit=False)
        skills_form.user = user
        skills_form.save(request=request)
    else:
        logger.error("Incorrect skills form...")
        if request.method == "GET":
            skills_form = SkillsForm(instance=obj)

    context = {
        'user': user,
        'skillsFORM': skills_form,
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def info_delete_view(request, id=None, *args, **kwargs):
    template_name = "user_interface/delete/information.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    if request.method == "POST" and id:
        info_obj = get_object_or_404(InformationModel, user=user, pk=id)
        info_obj.delete()
        logger.info(f"Deleted information for {user.username}...")
        info_obj = InformationModel.objects.filter(user=user).all()
        id = None
    else:
        info_obj = InformationModel.objects.filter(user=user).all()
        logger.info(f"Returning data for user: {user.username}...")

    context = {
        'user': user,
        "id": id,
        "information": info_obj
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def edu_delete_view(request, id, *args, **kwargs):
    template_name = "user_interface/delete/education.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    edu_obj = get_object_or_404(EducationModel, user=user, pk=id)

    if request.method == "POST" and id:
        edu_obj.delete

    context = {
        'user': user,
        "id": id
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def exp_delete_view(request, id, *args, **kwargs):
    template_name = "user_interface/delete/experience.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    exp_obj = get_object_or_404(ExperienceModel, user=user, pk=id)

    if request.method == "POST":
        exp_obj.delete

    context = {
        'user': user,
        "id": id
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def proj_delete_view(request, id, *args, **kwargs):
    template_name = "user_interface/delete/project.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    proj_obj = get_object_or_404(ProjectModel, user=user, pk=id)

    if request.method == "POST":
        proj_obj.delete

    context = {
        'user': user,
        "id": id
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def skill_delete_view(request, id=None, *args, **kwargs):
    template_name = "user_interface/delete/skillset.html"
    context = {}
    user = request.user
    logger.info(f"Reached delete route with method {request.method}...")

    if not user.is_authenticated:
        user = "admin"

    if request.method == "POST" and id:
        skill_obj = get_object_or_404(SkillsModel, user=user, pk=id)
        logger.info(f"Deleting Skillset object with id {id}")
        skill_obj.delete()
        skill_obj = SkillsModel.objects.filter(user=user).all()
        id = None
    else:
        skill_obj = SkillsModel.objects.filter(user=user).all()
        logger.info("Returning all skillset objects...")
    
    context = {
        'user': user,
        "id": id,
        "skills": skill_obj
    }

    return render(request, template_name, context)
