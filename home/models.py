from django.db import models
from froala_editor.fields import FroalaField
from userauth.models import Account
from django.utils import timezone

from django.conf import settings
User = settings.AUTH_USER_MODEL

class BlogData(models.Model):
    author=models.CharField(max_length=1000, null=True)
    domain=models.CharField(max_length=20, null=True)
    title=models.CharField(max_length=100, null=True)
    content=models.CharField(max_length=10000, null=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True)
    submitted_on = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.user) + str(self.submitted_on.strftime(f" - [%d %B %Y]"))

class ContactDetailsData(models.Model):
    email=models.CharField(max_length=100, null=True)
    subject=models.CharField(max_length=100, null=True)
    message=models.CharField(max_length=500, null=True)
    submitted_on = models.DateTimeField(default=timezone.now)
    
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.user) + self.submitted_on.strftime(f" - [%d %B %Y]")
    
class profileData(models.Model):
    name = models.CharField(max_length=100, null=True)
    domain_of_interest=models.CharField(max_length=100, null=True)
    dob=models.CharField(max_length=10, null=True)
    college_company=models.CharField(max_length=100, null=True)
    submitted_on = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name + self.submitted_on.strftime(f" - [%d %B %Y]")
    
    

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Image(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, unique=False)
    img = models.ImageField(upload_to='profile_pics/', default=None, null=True, unique=False)
    
    def __str__(self):
        return f'{self.user.fullname} Image'

class individualsData(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics/')
    
    def __str__(self):
        return f'{self.user.fullname} Profile'