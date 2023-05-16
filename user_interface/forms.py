from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import (User, InformationModel, EducationModel, ExperienceModel, ProjectModel, MessageModel, SkillsModel)


class IntroForm(ModelForm):
    class Meta:
        model = InformationModel
        fields = "__all__"


class EducationForm(forms.ModelForm):
    class Meta:
        model = EducationModel
        fields = ["user", "title", "year", "institute", "description"] 