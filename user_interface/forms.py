from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import (User, InformationModel, EducationModel, ExperienceModel, ProjectModel, MessageModel, SkillsModel)


# method one of creating the form model
class IntroForm(ModelForm):
    class Meta:
        model = InformationModel
        exclude = ('user',)

    def save(self, commit=True, *args, **kwargs):
        request = None
        if kwargs.__contains__("request"):
            request = kwargs.pop("request")
        m = super(IntroForm, self).save(commit=False, *args, **kwargs)
        if m.user is None and request is not None:
            m.user = request.user
            m.save()


# method two of creating the form model
class EducationForm(forms.ModelForm):
    class Meta:
        model = EducationModel
        exclude = ('user',)
        fields = ["user", "eduTitle", "course", "eduYear", "eduEndYear", "institute", "eduDescription"] 
        labels = {
            "user" : "User",
            "eduTitle": "Course Title",
            "eduYear": "Year",
            "institute": "University Name",
            "eduDescription": "Course Description"
        }

    def save(self, commit=True, *args, **kwargs):
        request = None
        if kwargs.__contains__("request"):
            request = kwargs.pop("request")
        m = super(EducationForm, self).save(commit=False, *args, **kwargs)
        if m.user is None and request is not None:
            m.user = request.user
            m.save()


class ExperienceForm(ModelForm):
    class Meta:
        model = ExperienceModel
        exclude = ('user',)
        fields = ["user", "expTitle", "expYear", "location", "expEndYear", "company", "expDescription"]
        labels = {
            "user": "User",
            "expTitle": "Job Title",
            "expYear": "Year",
            "company": "Company Name",
            "expDescription": "Job Description",
            "location": "Location"
        }

    def save(self, commit=True, *args, **kwargs):
        request = None
        if kwargs.__contains__("request"):
            request = kwargs.pop("request")
        m = super(ExperienceForm, self).save(commit=False, *args, **kwargs)
        if m.user is None and request is not None:
            m.user = request.user
            m.save()


class ProjectForm(ModelForm):
    class Meta:
        model = ProjectModel
        # fields = "__all__"
        exclude = ('user', 'slug', )
        labels = {
            "user" : "User",
            "projTitle": "Project Title",
            "projYear": "Year",
            "imagelink": "Image Link",
            "projDescription": "Project Description"
        }

    def save(self, commit=True, *args, **kwargs):
        request = None
        if kwargs.__contains__("request"):
            request = kwargs.pop("request")
        m = super(ProjectForm, self).save(commit=False, *args, **kwargs)
        if m.user is None and request is not None:
            m.user = request.user
            m.save()
  

class SkillsForm(ModelForm):
    class Meta:
        model = SkillsModel
        exclude = ('user',)

    def save(self, commit=True, *args, **kwargs):
        request = None
        if kwargs.__contains__("request"):
            request = kwargs.pop("request")
        m = super(SkillsForm, self).save(commit=False, *args, **kwargs)
        if m.user is None and request is not None:
            m.user = request.user
            m.save()


class MessageForm(ModelForm):
    class Meta:
        model = MessageModel
        fields = ["name", "email", "message", "subject"]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
    subject = forms.CharField(widget=forms.Textarea, max_length=2000)