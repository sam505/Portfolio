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
        fields = ["user", "eduTitle", "eduYear", "institute", "eduDescription"] 
        labels = {
            "user" : "User",
            "eduTitle": "Course Title",
            "eduYear": "Year",
            "institute": "University Name",
            "eduDescription": "Course Description"
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = ExperienceModel
        fields = ["user", "expTitle", "expYear", "company", "expDescription"]
        labels = {
            "user": "User",
            "expTitle": "Job Title",
            "expYear": "Year",
            "company": "Company Name",
            "expDescription": "Job Description"
        }


class ProjectForm(ModelForm):
    class Meta:
        model = ProjectModel
        # fields = "__all__"
        exclude = ('user', 'slug', )
  

class SkillsForm(ModelForm):
    class Meta:
        model = SkillsModel
        # fields = "__all__"
        exclude = ('user',)

    def save(self, commit=True, *args, **kwargs):
        request = None
        if kwargs.__contains__("request"):
            request = kwargs.pop("request")
        m = super(SkillsForm, self).save(commit=False, *args, **kwargs)
        if m.user == request.user:
            m.save()


class MessageForm(ModelForm):
    class Meta:
        model = MessageModel
        fields = ["name", "email", "message", "subject"]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
    subject = forms.CharField(widget=forms.Textarea, max_length=2000)