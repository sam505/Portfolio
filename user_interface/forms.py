from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import (User, InformationModel, EducationModel, ExperienceModel, ProjectModel, MessageModel, SkillsModel)


# method one of creating the form model
class IntroForm(ModelForm):
    class Meta:
        model = InformationModel
        fields = "__all__"


# method two of creating the form model
class EducationForm(forms.ModelForm):
    class Meta:
        model = EducationModel
        fields = ["user", "title", "year", "institute", "description"] 
        labels = {
            "user" : "User",
            "title": "Course Title",
            "year": "Year",
            "institute": "University Name",
            "description": "Course Description"
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = ExperienceModel
        fields = ["user", "title", "year", "company", "description"]
        labels = {
            "user": "User",
            "title": "Job Title",
            "year": "Year",
            "company": "Company Name",
            "description": "Job Description"
        }


class ProjectForm(ModelForm):
    class Meta:
        model = ProjectModel
        fields = "__all__"


class SkillsForm(ModelForm):
    class Meta:
        model = SkillsModel
        fields = "__all__"


class MessageForm(ModelForm):
    class Meta:
        model = MessageModel
        fields = ["name", "email", "message", "subject"]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
    subject = forms.CharField(widget=forms.Textarea, max_length=2000)