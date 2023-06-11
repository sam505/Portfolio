from django.db import models
from django.contrib.auth.models import AbstractUser
import re

# Create your models here.
class User(AbstractUser):
    pass


class InformationModel(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    userEmail = models.EmailField(blank=True, null=True)
    userPhone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatar/", blank=True, null=True)
    cv = models.FileField(upload_to="cv/", blank=True, null=True)

    # Social Links
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def save(self, **kwargs):
        if 'request' in kwargs and self.user is None:
            request = kwargs.pop('request')
            self.user = request.user
        super(InformationModel, self).save(**kwargs)

    def __str__(self) -> str:
        return f"{self.user} => {self.fullName}"
    

class EducationModel(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    eduTitle = models.CharField(max_length=50, blank=True, null=True)
    eduYear = models.CharField(max_length=50, blank=True, null=True)
    institute = models.CharField(max_length=100, blank=True, null=True)
    eduDescription = models.TextField(blank=True, null=True)

    
    class Meta:
        ordering = ["-eduYear"]
    
    def save(self, **kwargs):
        if 'request' in kwargs and self.user is None:
            request = kwargs.pop('request')
            self.user = request.user
        super(EducationModel, self).save(**kwargs)


    def __str__(self):
        return f"{self.user} => {self.eduTitle} from {self.institute}"
    


class ExperienceModel(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    expTitle = models.CharField(max_length=50, blank=True, null=True)
    expYear = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    expDescription = models.TextField(blank=True, null=True)

    
    class Meta:
        ordering = ["-expYear"]
    
    def save(self, **kwargs):
        if 'request' in kwargs and self.user is None:
            request = kwargs.pop('request')
            self.user = request.user
        super(ExperienceModel, self).save(**kwargs)


    def __str__(self):
        return f"{self.user} => {self.expTitle} from {self.company}"
    


class SkillsModel(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    skillTitle = models.CharField(max_length=50, blank=True, null=True)
    logolink = models.URLField(blank=True, null=True)
    skillDescription = models.TextField(blank=True, null=True)
    rank = models.CharField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)], default=2, max_length=10)


    class Meta:
        ordering = ["-rank"]


    def save(self, **kwargs):
        if 'request' in kwargs and self.user is None:
            request = kwargs.pop('request')
            self.user = request.user
        super(SkillsModel, self).save(**kwargs)


    def __str__(self) -> str:
        return f"{self.user} => {self.skillTitle} == {self.rank}"

    

class ProjectModel(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    projTitle = models.CharField(max_length=50, blank=True, null=True)
    # slug = models.SlugField(max_length=500, blank=True, null=True)
    projYear = models.CharField(max_length=50, blank=True, null=True)
    imagelink = models.URLField(blank=True, null=True)
    projDescription = models.TextField(blank=True, null=True)
    demo = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["-projYear"]


    def __str__(self) -> str:
        return f"{self.user} => {self.projTitle}"
    

    def get_project_absolute_url(self):
        return f"/project/{self.slug}"
    
    
    def save(self, **kwargs):
        # self.slug = self.slug_generate()
        if 'request' in kwargs and self.user is None:
            request = kwargs.pop('request')
            self.user = request.user
        super(ProjectModel, self).save(**kwargs)

    def slug_generate(self):
        slug = self.projTitle.strip()
        slug = re.sub("", "_", slug)

        return slug.lower()


class MessageModel(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=200, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    subject = models.CharField(max_length=1000, blank=False, null=False)
    send_time = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    class Meta:
        ordering = ["-send_time"]


    def save(self, **kwargs):
        if 'request' in kwargs and self.user is None:
            request = kwargs.pop('request')
            self.user = request.user
        super(MessageModel, self).save(**kwargs)


    def __str__(self) -> str:
        return f"{self.user} => {self.subject}"

