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
import math

logger.basicConfig(
    level=logger.INFO, 
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s'
                   )

# Create your views here.


def index(request):
    """Portfolio app landing page

    Args:
        request (dict): Request sent from the template html file

    Returns:
        render: Renders a html page 
    """

    return render(request, template_name="user_interface/index.html")


@login_required(login_url="login")
def form_create_view(request, *args, **kwargs):
    """Function to create new personal data for the user 

    Args:
        request (dict): Request data sent from the form template

    Returns:
        render: Form model or form model and captured errors
    """
    template_name = "user_interface/create/information.html"
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
    """Function called to create education information for the user

    Args:
        request (dict): Request sent from the template html page

    Returns:
        render: Education Form to be rendered on the create education template
    """
    template_name = "user_interface/create/education.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    # education form
    context = {
            'user': user,
            'eduFORM': EducationForm(),
        }
    edu_form = EducationForm(request.POST)
    if edu_form.is_valid():
        edu_form.save(commit=False)
        edu_form.user = user
        edu_form.save(request=request)

        if request.POST['add_object']=='Save & Proceed':
            return redirect('experience')
        else:
            return render(request, template_name, context)
    
    else:
        if request.method == "POST":
            context = {
                'user': user,
                'eduFORM': edu_form,
            }

        return render(request, template_name, context)


@login_required(login_url="login")
def form_create_experience_view(request, *args, **kwargs):
    """Function called by the create experience path

    Args:
        request (dict): _description_

    Returns:
        _type_: _description_
    """
    template_name = "user_interface/create/experience.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    # experience form
    context = {
                'user': user,
                'expFORM': ExperienceForm(),
            }
    exp_form = ExperienceForm(request.POST)
    if exp_form.is_valid():
        exp_form.save(commit=False)
        exp_form.user = user
        exp_form.save(request=request)

        if request.POST["add_object"] == "Save & Proceed":
            return redirect('project')
        else:
            return render(request, template_name, context)
    
    else:
        if request.method == "POST":
            context = {
                    'user': user,
                    'expFORM': exp_form,
                }

        return render(request, template_name, context)


@login_required(login_url="login")
def form_create_project_view(request, *args, **kwargs):
    template_name = "user_interface/create/project.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    # project form
    context = {
                'user': user,
                'projectFORM': ProjectForm(),
            }
    project_form = ProjectForm(request.POST, request.FILES)
    if project_form.is_valid():
        project_form.save(commit=False)
        project_form.user = user
        project_form.save(request=request)

        if request.POST["add_object"] == "Save & Proceed":
            return redirect('skillset')
        else:
            return render(request, template_name, context)
    
    else:
        if request.method == "POST":
            context = {
                'user': user,
                'projectFORM': project_form,
            }

        return render(request, template_name, context)


@login_required(login_url="login")
def form_create_skillset_view(request, *args, **kwargs):
    """Function called to create new skillset information

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    template_name = "user_interface/create/skillset.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    # skills form
    context = {
                'user': user,
                'skillsFORM': SkillsForm(),
            }
    skills_form = SkillsForm(request.POST, request.FILES)
    if skills_form.is_valid():
        skills_form.save(commit=False)
        skills_form.user = user
        skills_form.save(request=request)

        if request.POST["add_object"] == "Save & Proceed":
            return redirect('portfolio', user.username)
        else:
            return render(request, template_name, context)

    else:
        if request.method == "POST":
            context = {
                'user': user,
                'skillsFORM': skills_form,
            }

        return render(request, template_name, context)


def login_view(request, *args, **kwargs):
    """Function called when user attempts to login

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
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
            return render(request, "user_interface/loginRegister.html", {"message": "Wrong credentials! Try again."})

    else:
        logger.info("Logging in attempted with a different method...")
        return render(request, "user_interface/loginRegister.html")


def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse("login"))


def register_view(request, *args, **kwargs):
    """Function called when user is in the register page

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
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


def get_user_data(username: str):
    """A helper function to get a copy of all user data given their username

    Args:
        username (str): Username of the user

    Returns:
        dict: A dictionary containing all the user data
    """
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
    """Function called when the api method is accessed to show user data

    Args:
        request (_type_): _description_
        username (str): Username given in the url parameter

    Returns:
        _type_: _description_
    """
    context = get_user_data(username)

    return Response(context)


def portfolio_view(request, username, *args, **kwargs):
    """Function called to when the user navigates to their portfolio

    Args:
        request (dict): Request sent from the template
        username (str): Username of the user who is accessing their portfolio

    Returns:
        _type_: render template
    """
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
<<<<<<< HEAD
    """Function called when updating personal information form data
=======
    """Function called when updating users personal details
>>>>>>> cae3066 (Update docstring)

    Args:
        request (_type_): _description_

    Raises:
        Http404: _description_

    Returns:
        _type_: _description_
    """
    template_name = "user_interface/update/information.html"
    context = {}
    user = request.user
    logger.info("Updating Introduction Form...")
    if not user.is_authenticated:
        user = "admin"
    
    try:
        obj = InformationModel.objects.filter(user=user).first()
    except:
        return redirect("information")
    
    if request.method == "GET":
        info_form = IntroForm(instance=obj)
    
    elif request.method == "POST":
        # intro form
        info_form = IntroForm(request.POST, request.FILES, instance=obj)
        if info_form.is_valid():
            info_form.save(commit=False)
            info_form.user = user
            info_form.save(request=request)
            logger.info("Introduction form updated...")

            return redirect("update_education")
        else:
            logger.error(f"{request.method} Introduction form is Invalid...")
            

    context = {
        'user': user,
        'introFORM': info_form,
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def form_update_education_view(request, *args, **kwargs):
    """Function called to update existing education details

    Args:
        request (_type_): _description_

    Raises:
        Http404: _description_

    Returns:
        _type_: _description_
    """
    template_name = "user_interface/update/education.html"
    context = {}
    logger.info("Updating Education form...")
    user = request.user
    if not user.is_authenticated:
        user = "admin"
    
    ids = sorted(list(EducationModel.objects.filter(user=user).values_list('id', flat=True)))

    if request.method == "GET":
        try:
            obj = EducationModel.objects.get(id=ids[0])
            current_id = obj.id
            edu_form = EducationForm(instance=obj)
        except IndexError:
            return redirect("education")
        
    elif request.method == "POST":
        current_id = int(request.POST["id"])
        if len(ids) > 0:
            obj = EducationModel.objects.get(id=current_id)

            # education form
            edu_form = EducationForm(request.POST, instance=obj)
            if edu_form.is_valid() and request.method == "POST":
                edu_form.save(commit=False)
                edu_form.user = user
                edu_form.save(request=request)

                if request.POST["add_object"] == "Save & Proceed":
                    return redirect('update_experience')
                elif request.POST["add_object"] == "Save & Update Next":
                    idx = ids.index(current_id)
                    try:
                        current_id = ids[idx+1]
                        obj = EducationModel.objects.get(id=current_id)
                        edu_form = EducationForm(instance=obj)
            
                    except IndexError:
                        return redirect('update_experience')
    context = {
        'user': user,
        'eduFORM': edu_form,
        "id": current_id,
    }
    return render(request, template_name, context)

@login_required(login_url="login")
def form_update_experience_view(request, *args, **kwargs):
    """_summary_

    Args:
        request (_type_): _description_

    Raises:
        Http404: _description_

    Returns:
        _type_: _description_
    """
    template_name = "user_interface/update/experience.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    ids = sorted(list(ExperienceModel.objects.filter(user=user).values_list('id', flat=True)))
    
    if request.method == "GET":
        try:
            obj = ExperienceModel.objects.get(id=ids[0])
            current_id = obj.id
            exp_form = ExperienceForm(instance=obj)
        except IndexError:
            return redirect("experience")

    elif request.method == "POST":
        current_id = int(request.POST["id"])
        if len(ids) > 0:
            obj = ExperienceModel.objects.get(id=current_id)
            # experience form
            exp_form = ExperienceForm(request.POST, instance=obj)
            if exp_form.is_valid():
                exp_form.save(commit=False)
                exp_form.user = user
                exp_form.save(request=request)

                if request.POST["add_object"] == "Save & Proceed":
                    return redirect('update_project')
                elif request.POST["add_object"] == "Save & Update Next":
                    idx = ids.index(current_id)
                    try:
                        current_id = ids[idx+1]
                        obj = ExperienceModel.objects.get(id=current_id)
                        exp_form = ExperienceForm(instance=obj)

                    except IndexError:
                        return redirect("update_project")
                

    context = {
        'user': user,
        'expFORM': exp_form,
        "id": current_id,
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def form_update_project_view(request, *args, **kwargs):
    template_name = "user_interface/update/project.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    ids = sorted(list(ProjectModel.objects.filter(user=user).values_list("id", flat=True)))
    
    if request.method == "GET":
        try:
            obj = ProjectModel.objects.get(id=ids[0])
            current_id = obj.id
            project_form = ProjectForm(instance=obj)
        except:
            return redirect("project")
    
    elif request.method == "POST":
        current_id = int(request.POST["id"])
        if len(ids) > 0:
            obj = ProjectModel.objects.get(id=current_id)
            # project form
            project_form = ProjectForm(request.POST, request.FILES, instance=obj)
            if project_form.is_valid():
                project_form.save(commit=False)
                project_form.user = user
                project_form.save(request=request)

                if request.POST["add_object"] == "Save & Proceed":
                    return redirect('update_skillset')
                elif request.POST["add_object"] == "Save & Update Next":
                    idx = ids.index(current_id)
                    try:
                        current_id = ids[idx+1]
                        obj = ProjectModel.objects.get(id=current_id)
                        project_form = ProjectForm(instance=obj)
                    except IndexError:
                        return redirect("update_skillset")

    context = {
        'user': user,
        'projectFORM': project_form,
        "id": current_id,
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def form_update_skillset_view(request, *args, **kwargs):
    template_name = "user_interface/update/skillset.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    ids = sorted(list(SkillsModel.objects.filter(user=user).values_list("id", flat=True)))
    
    if request.method == "GET": 
        try:
            obj = SkillsModel.objects.get(id=ids[0])
            current_id = obj.id
            skills_form = SkillsForm(instance=obj)
        except:
            return redirect("skillset")
    
    elif request.method == "POST":
        current_id = int(request.POST["id"])
        if len(ids) > 0:
            obj = SkillsModel.objects.get(id=current_id)
    
            # skills form
            skills_form = SkillsForm(request.POST, request.FILES, instance=obj)
            if skills_form.is_valid():
                skills_form.save(commit=False)
                skills_form.user = user
                skills_form.save(request=request)

                if request.POST["add_object"] == "Save & Proceed":
                    return redirect("portfolio", user.username)
                elif request.POST["add_object"] == "Save & Update Next":
                    idx = ids.index(current_id)
                    try:
                        current_id = ids[idx+1]
                        obj = SkillsModel.objects.get(id=current_id)
                        skills_form = SkillsForm(instance=obj)

                    except IndexError:
                        return redirect("portfolio", user.username)

    context = {
        'user': user,
        'skillsFORM': skills_form,
        "id": current_id,
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
def edu_delete_view(request, id=None, *args, **kwargs):
    """_summary_

    Args:
        request (_type_): _description_
        id (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    template_name = "user_interface/delete/education.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    if request.method == "POST" and id:
        edu_obj = get_object_or_404(EducationModel, user=user, pk=id)
        edu_obj.delete()
        logger.info(f"Deleted education information for {user.username} and id: {id}...")
        edu_obj = EducationModel.objects.filter(user=user).all()
        id = None

    else:
        edu_obj = EducationModel.objects.filter(user=user).all()
        logger.info(f"Returning education data for user: {user.username}...")


    context = {
        'user': user,
        "id": id,
        "education": edu_obj
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def exp_delete_view(request, id=None, *args, **kwargs):
    """_summary_

    Args:
        request (_type_): _description_
        id (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    template_name = "user_interface/delete/experience.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    if request.method == "POST" and id:
        exp_obj = get_object_or_404(ExperienceModel, user=user, pk=id)
        exp_obj.delete()
        logger.info(f"Deleted experience information for {user.username} and id: {id}...")
        exp_obj = ExperienceModel.objects.filter(user=user).all()
        id = None

    else:
        exp_obj = ExperienceModel.objects.filter(user=user).all()
        logger.info(f"Returning experience data for user: {user.username}...")

    context = {
        'user': user,
        "id": id,
        "experience": exp_obj
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def proj_delete_view(request, id=None, *args, **kwargs):
    """_summary_

    Args:
        request (_type_): _description_
        id (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    template_name = "user_interface/delete/project.html"
    context = {}
    user = request.user
    if not user.is_authenticated:
        user = "admin"

    if request.method == "POST" and id:
        proj_obj = get_object_or_404(ProjectModel, user=user, pk=id)
        proj_obj.delete()
        logger.info(f"Deleted project information for {user.username} and id: {id}...")
        proj_obj = EducationModel.objects.filter(user=user).all()
        id = None

    else:
        proj_obj = ProjectModel.objects.filter(user=user).all()
        logger.info(f"Returning project data for user: {user.username}...")

    context = {
        'user': user,
        "id": id,
        "project": proj_obj
    }

    return render(request, template_name, context)


@login_required(login_url="login")
def skill_delete_view(request, id=None, *args, **kwargs):
    """_summary_

    Args:
        request (_type_): _description_
        id (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
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
