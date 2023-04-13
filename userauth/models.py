from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, fullname, email, domain, password):
        if not email:
            raise ValueError("User must have an email.")
        user = self.model(
            fullname = fullname,
            email = email,
            domain=domain,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, email, password):
        user = self.create_user(
            fullname = fullname,
            email = email,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Create your models here.
class Account(AbstractBaseUser):
    email           = models.EmailField(max_length=50, unique =True, null=True)
    fullname        = models.CharField(max_length=20, null=True)
    domain          = models.CharField(max_length=20, null=True)
    is_admin        = models.BooleanField(default=False, null=True)
    is_active       = models.BooleanField(default=True,null=True)
    is_staff        = models.BooleanField(default=False,null=True)
    is_superuser    = models.BooleanField(default=False,null=True)
    date_joined     = models.DateTimeField(verbose_name="date joined", auto_now_add=True,null=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname',]

    def __str__(self):
        return self.fullname
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True