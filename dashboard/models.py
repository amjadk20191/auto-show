from django.db import models

# Create your models here.
class Category(models.Model):
    Name=models.CharField(max_length=50)
    Description=models.TextField()
    

