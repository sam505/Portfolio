from django.db import models
from django.contrib.auth.models import AbstractUser
import re

# Create your models here.
class User(AbstractUser):
    pass


class InformationModel(models.Model):
    user = models.ForeignKey(User, default=None, blank=False, null=True, on_delete=models.CASCADE)
    fName = models.CharField(max_length=50, blank=False, null=True)
    lName = models.CharField(max_length=50, blank=False, null=True)
    bio = models.CharField(max_length=500, blank=False, null=True)
    about = models.TextField(blank=False, null=True)
    address = models.CharField(max_length=100, blank=False, null=True)
    userEmail = models.EmailField(blank=False, null=True)
    dob = models.DateField(max_length=50, blank=True, null=True, default="")
    userPhone = models.CharField(max_length=15, blank=False, null=True)
    avatar = models.ImageField(upload_to="avatar/", blank=False, null=True)
    cv = models.FileField(upload_to="cv/", blank=False, null=True)

    # Social Links
    github = models.URLField(blank=True, null=True, default="")
    linkedin = models.URLField(blank=True, null=True, default="")
    stackoverflow = models.URLField(blank=True, null=True, default="")
    facebook = models.URLField(blank=True, null=True, default="")
    twitter = models.URLField(blank=True, null=True, default="")


    def save(self, **kwargs):
        if 'request' in kwargs and self.user is None:
            request = kwargs.pop('request')
            self.user = request.user
        super(InformationModel, self).save(**kwargs)

    def __str__(self) -> str:
        return f"{self.user} => {self.fName} {self.lName}"
    

class EducationModel(models.Model):
    user = models.ForeignKey(User, default=None, blank=False, null=True, on_delete=models.CASCADE)
    eduTitle = models.CharField(max_length=50, blank=False, null=True)
    course = models.CharField(max_length=50, blank=False, null=True)
    eduYear = models.DateField(max_length=50, blank=False, null=True)
    eduEndYear = models.DateField(max_length=50, blank=False, null=True)
    institute = models.CharField(max_length=100, blank=False, null=True)
    eduDescription = models.TextField(blank=True, null=True, default="")

    
    class Meta:
        ordering = ["-eduYear"]
    
    def save(self, **kwargs):
        if 'request' in kwargs and self.user is None:
            request = kwargs.pop('request')
            self.user = request.user
        super(EducationModel, self).save(**kwargs)


    def startyear(self):
        return self.eduYear.strftime('%Y')
    
    def endyear(self):
        return self.eduEndYear.strftime('%Y')
    
    def __str__(self):
        return f"{self.user} => {self.eduTitle} from {self.institute}"
    


class ExperienceModel(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    expTitle = models.CharField(max_length=50, blank=False, null=True)
    expYear = models.DateField(max_length=50, blank=False, null=True)
    expEndYear = models.DateField(max_length=50, blank=False, null=True)
    company = models.CharField(max_length=100, blank=False, null=True)
    location = models.CharField(max_length=100, blank=False, null=True)
    expDescription = models.TextField(blank=False, null=True)

    
    class Meta:
        ordering = ["-expYear"]

    def startyear(self):
        return self.expYear.strftime('%Y')
    
    def endyear(self):
        return self.expEndYear.strftime('%Y')
    
    def save(self, **kwargs):
        if 'request' in kwargs and self.user is None:
            request = kwargs.pop('request')
            self.user = request.user
        super(ExperienceModel, self).save(**kwargs)

    def __str__(self):
        return f"{self.user} => {self.expTitle} at {self.company}"
    


class SkillsModel(models.Model):
    user = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.CASCADE)
    skillTitle = models.CharField(max_length=50, blank=False, null=True)
    logolink = models.ImageField(upload_to="skills/", blank=False, null=True)
    skillDescription = models.TextField(blank=False, null=True)
    rank = models.CharField(choices=[('1',1), ('2',2), ('3',3), ('4',4), ('5',5)], default=3, max_length=10)


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
    projTitle = models.CharField(max_length=50, blank=False, null=True)
    projYear = models.CharField(max_length=50, blank=False, null=True)
    imagelink = models.ImageField(upload_to="projects/", blank=False, null=True)
    projDescription = models.TextField(blank=False, null=True)
    demo = models.URLField(blank=False, null=True)
    github_link = models.URLField(blank=False, null=True)

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

