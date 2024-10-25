from django.db import models
import uuid

from dashboard.models import Category
from rest_framework.exceptions import APIException
from core.utils import CheckPhoneNumber
import os
from car_dealerships import settings


class AutoShow(models.Model):
    Name=models.CharField(max_length=100)
    Address=models.TextField()
    Image=models.FileField(upload_to=f'AutoShow/{str(uuid.uuid4())}%Y%m%d',blank=True,null=True)
    MinPrice=models.FloatField(default=0)
    MaxPrice=models.FloatField(default=999_999_999_999_999_999_999)
    CreatedAt = models.DateField(auto_now_add=True, blank=True)
    StartAt = models.DateField()
    EndAt = models.DateField()
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    Posting = models.PositiveIntegerField(default=0,blank=True)
    Phone = models.CharField(max_length=30)
    Latitude = models.FloatField()
    Logitude = models.FloatField()
    Category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def delete(self, *args, **kwargs):


        try:
           image_path = self.Image.path

           if os.path.exists(image_path):
               os.remove(image_path)
        except:
            pass
        Car.objects.only("pk","Sold").filter(AutoShow__pk=self.pk).filter(Sold=False).delete()

        super(AutoShow, self).delete(*args, **kwargs)
        

    

class Car(models.Model): 
    Name=models.CharField(max_length=255)
    Model=models.CharField(max_length=255)
    Color=models.CharField(max_length=50)
    Price=models.FloatField()
    Phone=models.CharField( max_length=30)
    AutoShow = models.ForeignKey(AutoShow, on_delete=models.SET_NULL,null=True)
    Address=models.TextField()
    Miles=models.FloatField(default=0)
    Gear=models.CharField(max_length=255)
    CreatedAt = models.DateField(auto_now_add=True, blank=True)
    ManufacturedAt = models.IntegerField()
    Status = models.CharField(max_length=100)
    Cylinder = models.CharField(max_length=100)
    Wheels = models.IntegerField()
    Chairs = models.IntegerField()
    Type=models.CharField(max_length=100)
    Description=models.TextField()
    CC=models.FloatField()
    Sold=models.BooleanField(default=False)
    Latitude=models.FloatField()
    Logitude=models.FloatField()
    Furnaiture = models.TextField()
    Roof= models.TextField()    
    Seller= models.TextField()    
    Fuel= models.TextField()    
    Number= models.TextField()    
    Paint= models.TextField()    
    Lock= models.TextField()   
    Views=models.BigIntegerField(default=0) 
    Year=models.IntegerField()
    def delete(self, *args, **kwargs):
        print(";;;;;;;;;;;;;;;;;;")

        if hasattr(self,"_prefetched_objects_cache"):
            for image in self._prefetched_objects_cache["carimages_set"]:
                try:
                    image_path = image.Image.path
                    print(image_path)
                    if os.path.exists(image_path):
                        print("yeeeeeeeeeeee")
                        os.remove(image_path)
                except:
                    pass
        else:
            images=CarImages.objects.values("Image").filter(Car__pk=self.pk)
            for image in images:
                try:
                    image_path = os.path.join(settings.MEDIA_ROOT,image["Image"])
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except:
                    pass

        if not self.Sold:
            print(";;;;;;;;;;;;;;;;;;;;;;")
            super(Car, self).delete(*args, **kwargs)
        


    

class CarImages(models.Model): 
    Car = models.ForeignKey(Car, on_delete=models.CASCADE)
    Image=models.FileField(upload_to=f'Cars/{str(uuid.uuid4())}%Y%m%d')

 
    def delete(self, *args, **kwargs):
        try:
           image_path = self.Image.path
           if os.path.exists(image_path):
               os.remove(image_path)
        except:
            pass

        
        return super().delete(*args, **kwargs)
        

 
    