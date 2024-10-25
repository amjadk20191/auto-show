
import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin,AnonymousUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import  MinValueValidator
from Auto_Show.models import AutoShow
from core.utils import CheckPhoneNumber

from .manager import UserManager

import os

class User(AbstractBaseUser, PermissionsMixin):

    Name=models.CharField(max_length=50)
    Image=models.FileField(upload_to=f'usersProfile/{str(uuid.uuid4())}%Y%m%d',blank=True,null=True)
    Username=models.CharField( max_length=50,unique=True)
    Phone=models.CharField(max_length=30)
    Group=models.CharField(max_length=30)
    Address=models.TextField()
    AutoShow = models.OneToOneField(AutoShow, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
   
    objects = UserManager()
    def delete(self, *args, **kwargs):
        try:
           image_path = self.Image.path
           if not image_path is None:
                if os.path.exists(image_path):
                    os.remove(image_path)
           if hasattr(self,"AutoShow"):
                if not self.AutoShow is None:

                    image_path = self.AutoShow.Image.path
                    if os.path.exists(image_path):
                        os.remove(image_path)

                    self.AutoShow.delete()

                    return
        except:
            pass

        super(User,self).delete(*args, **kwargs)
        

 
   
    USERNAME_FIELD = 'Username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')