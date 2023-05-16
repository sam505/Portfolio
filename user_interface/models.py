from django.db import models
from django.contrib.auth.models import AbstractUser
import re

# Create your models here.
class User(AbstractUser):
    pass


class InformationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatar/", blank=True, null=True)
    cv = models.FileField(upload_to="cv/", blank=True, null=True)

    # Social Links
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)


    def __str__(self) -> str:
        return self.full_name
    

class EducationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    institute = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    class Meta:
        ordering = ["-year"]


    def __str__(self):
        return f"{self.user} => {self.title} from {self.institute}"
    


class ExperienceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    class Meta:
        ordering = ["-year"]


    def __str__(self):
        return f"{self.user} => {self.title} from {self.company}"
    


class SkillsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    imagelink = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rank = models.CharField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)], default=2, max_length=10)

    class Meta:
        ordering = ["-rank"]


    def __str__(self) -> str:
        return f"{self.user} => {self.title} == {self.rank}"

    

class ProjectModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=500, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    imagelink = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    demo = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["-year"]


    def __str__(self) -> str:
        return f"{self.user} => {self.title}"
    

    def get_project_absolute_url(self):
        return f"/project/{self.slug}"
    
    
    def save(self, *args, **kwargs):
        self.slug = self.slug_generate()
        super(ProjectModel, self).save(*args, **kwargs)

    def slug_generate(self):
        slug = self.title.strip()
        slug = re.sub("", "_", slug)

        return slug.lower()


class MessageModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=200, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    subject = models.CharField(max_length=1000, blank=False, null=False)
    send_time = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    class Meta:
        ordering = ["-send_time"]

    def __str__(self) -> str:
        return f"{self.user} => {self.subject}"

