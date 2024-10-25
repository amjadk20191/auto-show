from rest_framework.response import Response
from rest_framework import generics,viewsets,views
from .models import Category
from core.models import User
from .serializers import (CategorySerializer, UserAdminSerializer, UserAuto_ShowSerializer, ImageSerializer,
                           CarSerializer, Auto_ShowSerializer, UserAutoShowAdminSerializer, CarUpdateSerializer,
                           CarSubSerializer, AutoShowSubSerializer,CategoryWithAutoShowSerializer)
from rest_framework import status
from Auto_Show.models import AutoShow, Car, CarImages
from core.utils import CheckPhoneNumber
from django.contrib.auth.hashers import make_password
from django.db.models import F
from django.db.models import ProtectedError
from car_dealerships import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
import uuid
import os
from django.db import IntegrityError
from django.db import transaction, connection
from django.forms.models import model_to_dict 
import json
from core.pagination import DefaultPagination
from django.db.models import Prefetch


class CategoryViewset(viewsets.ModelViewSet):
    
    http_method_names=['get','delete','patch','post']
    serializer_class = CategorySerializer
    queryset=Category.objects.all()
    # pagination_class=DefaultPagination





    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         return super().destroy(request, *args, **kwargs)
    #     except ProtectedError:
    #         return Response({"detail":"the Category has Auto Show"},status=status.HTTP_400_BAD_REQUEST)
   
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            pk = int(pk)
        except (ValueError, TypeError):
            return Response(
            {"detail": "Invalid ID. ID must be an integer."},status=status.HTTP_400_BAD_REQUEST)
        validToDelete=AutoShow.objects.filter(Category__pk=pk).exists()
        print(validToDelete)
        if not validToDelete:
            sql = "DELETE FROM dashboard_Category WHERE id = %s"

            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(sql, [pk])
                    if cursor.rowcount == 0:
                        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "this Category has Auto Show"}, status=status.HTTP_404_NOT_FOUND)


class UserAdminViewset(viewsets.ModelViewSet):
    
    http_method_names=['get','delete','patch','post']
    serializer_class = UserAdminSerializer
    queryset=User.objects.only('pk','Name','Image','Username','Phone','Address','AutoShow_id').filter(Group="admin")
    # pagination_class=DefaultPagination

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(User(pk=kwargs['pk']),data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data=serializer.validated_data
        
        if "Phone"in validated_data:
            CheckPhoneNumber(validated_data['Phone'])

        if 'password' in validated_data:  
            validated_data['password']=make_password(validated_data['password'])

        try:
            if 'Image' in validated_data :  
                user_Image=User.objects.values("Image").filter(pk=kwargs['pk']).first()
                if not user_Image is None:
                    if not validated_data["Image"] is None:
                        Now = datetime.now()

                        DateTime = Now.strftime("%m%d%Y%H%M%S")
                        validated_data['Image'] = default_storage.save(f'usersProfile/{str(uuid.uuid4())}{DateTime}'+validated_data['Image'].name, ContentFile(validated_data['Image'].read()))
                    if not user_Image["Image"] is None:

                        old_image_path=os.path.join(settings.MEDIA_ROOT,user_Image["Image"])
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                else: 
                    return Response({"detail":"the user does not exist"},status=status.HTTP_400_BAD_REQUEST)
           
        except:
                pass
        

        User.objects.filter(pk=kwargs['pk']).update(**validated_data)

        if "Image" in validated_data and(not validated_data["Image"] is None): 
                validated_data["Image"]=request.build_absolute_uri('/') +\
                    os.path.join(settings.MEDIA_URL[1:],validated_data["Image"] )


        return Response(validated_data)

    
class UserAutoShowViewset(viewsets.ModelViewSet):
    
    http_method_names=['delete','post']
    serializer_class = UserAuto_ShowSerializer
    queryset=User.objects.select_related('AutoShow').only('pk','Name','Image','Username','Phone','Address','password','AutoShow',
                                                            'AutoShow__id','AutoShow__Name','AutoShow__Address','AutoShow__Image','AutoShow__StartAt','AutoShow__StartTime','AutoShow__EndTime','AutoShow__EndAt','AutoShow__Posting','AutoShow__Phone','AutoShow__Latitude','AutoShow__Logitude','AutoShow__Category_id'
                                                            )\
                                                            .annotate(AutoShow_pk=F('AutoShow__id'),AutoShow_Name=F('AutoShow__Name'),AutoShow_Address=F('AutoShow__Address')
                                                                      ,AutoShow_Image=F('AutoShow__Image'),AutoShow_StartAt=F('AutoShow__StartAt'),AutoShow_EndAt=F('AutoShow__EndAt'),AutoShow_StartTime=F('AutoShow__StartTime'),AutoShow_EndTime=F('AutoShow__EndTime'),
                                                                      AutoShow_Posting=F('AutoShow__Posting'),AutoShow_Phone=F('AutoShow__Phone'),AutoShow_Latitude=F('AutoShow__Latitude'),
                                                                      AutoShow_Logitude=F('AutoShow__Logitude'),AutoShow_Category_id=F('AutoShow__Category_id'))\
   
    def destroy(self, request, *args, **kwargs):
        print(kwargs)
        pk = kwargs.get('pk')
        print(pk)
        try:
            pk = int(pk)
        except (ValueError, TypeError):
            return Response(
            {"detail": "Invalid ID. ID must be an integer."},status=status.HTTP_400_BAD_REQUEST)
        print("llllllllllllllllllll")
        user=User.objects.select_related('AutoShow').values('pk','AutoShow__id','Image','AutoShow__Image').filter(pk=pk,Group="AutoShow").first()
        print("llllllllllllllllllll")
        print(user)

        if user is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        print("llllllllllllllllllll")
        deleteCar=False

        cars=Car.objects.values('pk').filter(AutoShow__pk=user["AutoShow__id"])
        cars_pk=[car['pk'] for car in cars]
        print(cars)
        print("pppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
        print(len(cars))
        print("pppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
        if len(cars)>0:
            Images=list(CarImages.objects.values('Image').filter(Car__in=cars_pk))
            deleteCar=True
            print(Images)
            placeholders = ','.join(['%s'] * len(cars_pk))

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                   
                    if deleteCar:

                        sql = f"DELETE FROM Auto_Show_CarImages WHERE Car_id IN ({placeholders})"
                        cursor.execute(sql, cars_pk)
                    

                        sql = "DELETE FROM Auto_Show_Car WHERE AutoShow_id = %s AND Sold=false"
                        cursor.execute(sql, [user["AutoShow__id"]])
                    
                    sql = "DELETE FROM django_admin_log WHERE user_id = %s"
                    cursor.execute(sql, [user["pk"]])

                    sql = "DELETE FROM core_user_groups WHERE user_id = %s"
                    cursor.execute(sql, [user["pk"]])

                    sql = "DELETE FROM core_user_user_permissions WHERE user_id = %s"
                    cursor.execute(sql, [user["pk"]])
                    sql = "DELETE FROM Auto_Show_AutoShow WHERE id = %s"
                    cursor.execute(sql, [user["AutoShow__id"]])
                    sql = "DELETE FROM core_user WHERE id = %s"
                    cursor.execute(sql, [user["pk"]])

                    sql = "UPDATE Auto_Show_car SET AutoShow_id = NULL WHERE AutoShow_id= %s"
                    cursor.execute(sql, [user["AutoShow__id"]])




                    if deleteCar:
                        for Image in Images:
                            try:
                                path=os.path.join(settings.MEDIA_ROOT,Image["Image"])
                                if os.path.exists(path):
                                    print("car")
                                    os.remove(path)
                            except:
                                pass
                        try:
                            path=os.path.join(settings.MEDIA_ROOT,user["Image"])
                            if os.path.exists(path):
                                print("user")
                                os.remove(path)
                        except:
                            pass
                        try:
                            path=os.path.join(settings.MEDIA_ROOT,user["AutoShow__Image"])
                            if os.path.exists(path):
                                print("aaaa")
                                os.remove(path)
                        except:
                            pass

                        
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST)




class AutoShowViewset(viewsets.ModelViewSet):
    
    http_method_names=['patch','get']
    serializer_class = Auto_ShowSerializer
    queryset=AutoShow.objects.select_related('Category').only('Category__Name',
                                                                'pk','Name','Address','Image','StartAt','EndAt','Posting','Phone','Latitude','Logitude','StartTime','EndTime','MinPrice','MaxPrice','user')\
                                                        .annotate(Category_Name=F('Category__Name'))\
                                                        .all()
    # pagination_class=DefaultPagination
    def update(self, request, *args, **kwargs):
        data_AutoShow=AutoShow.objects.values("Image","StartAt","EndAt").filter(pk=kwargs['pk']).first()

        if(data_AutoShow is None):
            return Response({"detail":"there is no Auto Show"},status=status.HTTP_404_NOT_FOUND)
        EndAt=data_AutoShow['EndAt']
        StartAt=data_AutoShow['StartAt']

        serializer = self.get_serializer(AutoShow(pk=kwargs['pk']),data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data=serializer.validated_data
        print(validated_data)

        if "StartAt" in validated_data:
            StartAt=validated_data['StartAt']
        if "EndAt" in validated_data:
            EndAt=validated_data['EndAt']
        if(StartAt < EndAt):
            return Response({"detail":"StartAt is biger than EndAt"},status=status.HTTP_400_BAD_REQUEST)

        
        
        if ('Image' in validated_data) and (not validated_data["Image"] is None):  

            Now = datetime.now()
            DateTime = Now.strftime("%m%d%Y%H%M%S")
            newImagePath=f'AutoShow/{str(uuid.uuid4())}{DateTime}'+validated_data['Image'].name
            validated_data['Image'] = default_storage.save(newImagePath, ContentFile(validated_data['Image'].read()))
        if "Category" in validated_data:

            validated_data["Category"]=Category(pk=validated_data["Category"])
        try:

            AutoShow.objects.filter(pk=kwargs['pk']).update(**validated_data)
        except IntegrityError:
            if 'Image' in validated_data :
                
                if os.path.exists(newImagePath):
                    os.remove(newImagePath)  

            return Response({"detail":"Category is not exist."},status=status.HTTP_400_BAD_REQUEST)
        try:    
            if 'Image' in validated_data :  
                if not data_AutoShow["Image"] is None:
                    old_image_path=os.path.join(settings.MEDIA_ROOT,data_AutoShow["Image"])

                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                    if(not validated_data["Image"] is None): 
                        validated_data["Image"]=request.build_absolute_uri('/') +\
                            os.path.join(settings.MEDIA_URL[1:],validated_data["Image"] )

        except:
            pass
        if "Category" in validated_data:

            validated_data.pop("Category")
        return Response(validated_data)
                                                            
    

class AutoShowSubViewset(viewsets.ModelViewSet):
    
    http_method_names=['get']
    serializer_class = AutoShowSubSerializer
    queryset=AutoShow.objects.select_related('Category').only('Category__Name',
                                                                'pk','Name','Address','Image','StartAt','StartTime','EndTime',)\
                                                        .annotate(Category_Name=F('Category__Name'))\
                                                        .all()


class UserAutoShowAdminViewset(viewsets.ModelViewSet):
    
    http_method_names=['get','patch']
    serializer_class = UserAutoShowAdminSerializer
    queryset=User.objects.only('pk','Name','Image','Username','Phone','Address').filter(Group="AutoShow")
    # pagination_class=DefaultPagination

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(User(pk=kwargs['pk']),data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data=serializer.validated_data
        
        if "Phone"in validated_data:
            CheckPhoneNumber(validated_data['Phone'])

        if 'password' in validated_data:  
            validated_data['password']=make_password(validated_data['password'])

        try:
            if 'Image' in validated_data :  
                user_Image=User.objects.values("Image").filter(pk=kwargs['pk']).first()
                if not user_Image is None:
                    if not validated_data["Image"] is None:
                        Now = datetime.now()

                        DateTime = Now.strftime("%m%d%Y%H%M%S")
                        validated_data['Image'] = default_storage.save(f'usersProfile/{str(uuid.uuid4())}{DateTime}'+validated_data['Image'].name, ContentFile(validated_data['Image'].read()))
                    if not user_Image["Image"] is None:

                        old_image_path=os.path.join(settings.MEDIA_ROOT,user_Image["Image"])
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                else: 
                    return Response({"detail":"the user does not exist"},status=status.HTTP_400_BAD_REQUEST)
           
        except:
                pass
        

        User.objects.filter(pk=kwargs['pk']).update(**validated_data)

        if "Image" in validated_data and(not validated_data["Image"] is None): 
                validated_data["Image"]=request.build_absolute_uri('/') +\
                    os.path.join(settings.MEDIA_URL[1:],validated_data["Image"] )


        return Response(validated_data)
             

class carViewset(viewsets.ModelViewSet):
    
    http_method_names=['get','patch','post','delete']
    serializer_class = CarSerializer
    pagination_class=DefaultPagination
    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('autoshow')
        print(pk)
        print(self.request.method)
        if self.request.method == 'DELETE':
            self.queryset =Car.objects.prefetch_related('carimages_set').only(
                                                                'pk',"Sold")\
                                                            .filter(AutoShow=pk)
        
        if self.request.method == 'PATCH':
                                        self.queryset =Car.objects.only(
                                                    'pk','Name','Model','Color','Price','Phone','Miles','Gear','CreatedAt','ManufacturedAt',
                                                    'Status','Cylinder','Wheels','Chairs','Type','Description','CC','Sold','Latitude','Logitude',
                                                    'Furnaiture','Roof','Seller','Fuel','Number','Paint','Lock','Year')\
                                                .filter(AutoShow=pk)
        else:
            self.queryset =Car.objects.prefetch_related('carimages_set').only(
                                                                'pk','Name','Model','Color','Price','Phone','Miles','Gear','CreatedAt','ManufacturedAt',
                                                                'Status','Cylinder','Wheels','Chairs','Type','Description','CC','Sold','Latitude','Logitude',
                                                                'Furnaiture','Roof','Seller','Fuel','Number','Paint','Lock','Year')\
                                                            .filter(AutoShow=pk)
        return super().get_queryset()
    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'PATCH':
            return CarUpdateSerializer(*args, **kwargs)

        return super().get_serializer(*args, **kwargs)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data=serializer.validated_data
       


        autoshowpk=kwargs['autoshow']
        validated_data['AutoShow']=AutoShow(pk=autoshowpk)
        print(validated_data)
        CarImages_data=validated_data.pop("carimages_set")
        imagesCount=len(CarImages_data)
        if (not imagesCount<10):
                return Response({"detail":"images is more than should"},status=status.HTTP_400_BAD_REQUEST)

        if (not imagesCount>0):
                return Response({"detail":"shoud send one image at less"},status=status.HTTP_400_BAD_REQUEST)

        
                
        try:
            with transaction.atomic():

            
                    car=Car.objects.create(**validated_data)
                    car_images_instances = [
                            CarImages(Car=car, **image_data) for image_data in CarImages_data]
                    carimages=CarImages.objects.bulk_create(car_images_instances,batch_size=10)
                    car=model_to_dict(car)


            return Response(car,status=status.HTTP_201_CREATED)
        except IntegrityError:
                return Response({"detail":"Auto Show is not exist"},status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(Car(pk=kwargs['pk']),data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data=serializer.validated_data
        Car.objects.filter(pk=kwargs['pk']).update(**validated_data)
        return Response(validated_data)


class ImageViewset(viewsets.ModelViewSet):
    
    http_method_names=['get','post','delete']######################### shel get
    serializer_class = ImageSerializer
    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pkcar')
        self.queryset=CarImages.objects.only('pk','Image').filter(Car__pk=pk)
        return super().get_queryset()

    
    def create(self, request, *args, **kwargs):
        ImagesNumber=CarImages.objects.filter(Car__pk=kwargs['pkcar']).count()
        serializer = self.get_serializer(data=request.data ,many=True)
        serializer.is_valid(raise_exception=True)
        validated_data=serializer.validated_data
        
        if ImagesNumber+len(validated_data)>10:
            return Response({"detail":"You have reached the maximum number of images."},status=status.HTTP_400_BAD_REQUEST)
        
        car=Car(pk=kwargs['pkcar'])
        car_images_instances = [
                            CarImages(Car=car, **image_data) for image_data in validated_data]
        try:
            CarImages.objects.bulk_create(car_images_instances,batch_size=10)
        except IntegrityError:
                return Response({"detail":"Car is not exist"},status=status.HTTP_400_BAD_REQUEST)



        return Response(
            {}
            ,status=status.HTTP_201_CREATED)



class carsubViewset(viewsets.ModelViewSet):
    
    http_method_names=['get']
    serializer_class = CarSubSerializer
    pagination_class=DefaultPagination
    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('autoshow')
        self.queryset =Car.objects.prefetch_related('carimages_set').only(
                                                                'pk','Name','Model','Color','Price','Gear','CreatedAt')\
                                                            .filter(AutoShow=pk)
        return super().get_queryset()


class CategoryWithAutoShowViewset(viewsets.ModelViewSet):
    
    http_method_names=['get',]
    serializer_class = CategoryWithAutoShowSerializer
    autoshow_queryset = AutoShow.objects.only('pk','Name','Address','Image','StartAt','StartTime','EndTime','Category')

    queryset=Category.objects.prefetch_related(
         Prefetch('autoshow_set', queryset=autoshow_queryset)
    ).only("Name","Description").all()