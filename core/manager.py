
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import APIException
import re
import os

from .utils import CheckPhoneNumber

class UserManager(BaseUserManager):
    use_in_migrations = True




    def create(self, password=None, **extra_fields):
        
        extra_fields['Phone'] = CheckPhoneNumber(extra_fields['Phone'])
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, password, **extra_fields):
        
        
        if 'Phone' in  extra_fields:
            extra_fields['Phone'] = CheckPhoneNumber(extra_fields['Phone'])
        user = self.model(**extra_fields)

        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.group='admin'

        user.save(using=self._db)
        return user



    def update(self,**kwargs):
        
        if "Phone"in kwargs:
            CheckPhoneNumber(kwargs['Phone'])

        if 'password' in kwargs:  
                kwargs['password']=make_password(kwargs['password'])

        try:    
                if 'Image' in kwargs :  
                        old_image_path=instance.Image.path
                
                        if os.path.exists(old_image_path):
                                os.remove(old_image_path)
        except:
                pass

        return super().update(**kwargs)
