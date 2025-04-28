from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from .managers import UserManager
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'                       # the field you wish to do authentication
    REQUIRED_FIELDS = ["email", "full_name"]                             # includes when you make a super user

    def __str__(self):
        return self.email
    
    # checks if each users (exist in db) has permission to any (obj) module.
    #def has_perm(self, perm, obj=None):                     # any specific permission
    #    return True
    #
    #def has_module_perms(self, app_label):                   # permission to view any particular module
    #    return True
    
    # if the user has a True is_staff it has access to admin pannel 
    @property
    def is_staff(self):                                     # check if the user is admin or not
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {self.code} - {self.created}"
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if not user:
            raise ValidationError("This Email Has Already Exists!")
        return email

    def clearn_phone(self):
        phone = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone).exists()
        if not user:
            raise ValidationError("This Phone-Number Has Already Used!")
        OtpCode.objects.filet(phone_number=phone).delete()
        return phone