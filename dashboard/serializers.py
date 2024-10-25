from rest_framework import serializers
from .models import Category
from core.models import User
from django.contrib.auth.hashers import make_password
from core.utils import CheckPhoneNumber
from Auto_Show.models import AutoShow, Car, CarImages
from django.db import transaction
from django.db import IntegrityError
from core.utils import CheckPhoneNumber
from drf_extra_fields.fields import Base64ImageField

class CategorySerializer(serializers.ModelSerializer):
        class Meta:
                model = Category
                fields = '__all__'
    
    
    

class UserAdminSerializer(serializers.ModelSerializer):
        password = serializers.CharField(style={"input_type": "password"},write_only=True)
        Image=Base64ImageField()

        class Meta:
                model = User
                fields = ['pk','Name','Image','Username','Phone','Address','password']

        def create(self, validated_data):

                validated_data['Group']='admin'    
                data=super().create(validated_data)
                return data
  


class AutoShowSerializer(serializers.ModelSerializer):
        Category_id=serializers.IntegerField()
        Image=Base64ImageField()

        class Meta:
                model = AutoShow
                fields = ['pk','Name','Address','Image','StartAt','EndAt','StartTime','EndTime','Posting','Phone','Latitude','Logitude','Category_id']


class UserAuto_ShowSerializer(serializers.ModelSerializer):
        password = serializers.CharField(style={"input_type": "password"},write_only=True)
        AutoShow =AutoShowSerializer()
        Image=Base64ImageField()


        class Meta:
                model = User
                fields = ['pk','Name','Image','Username','Phone','Address','password','AutoShow']
        
        # @transaction.atomic()
        def create(self, validated_data):

                auto_show_data = validated_data.pop('AutoShow')
                auto_show_data['Category']=Category(pk=auto_show_data.pop("Category_id"))
                auto_show_data['Phone'] = CheckPhoneNumber(auto_show_data['Phone'])

                try:
                    with transaction.atomic():

                        auto_show=AutoShow.objects.create(**auto_show_data)
                        validated_data['Group']='AutoShow'    
                        validated_data['AutoShow']=auto_show 

                        user=super().create(validated_data)
                        return user              
                except IntegrityError:
                        raise serializers.ValidationError({"detail":"Category is not exist."})


class Auto_ShowSerializer(serializers.ModelSerializer):
        Category_Name=serializers.CharField(read_only=True)
        Category=serializers.IntegerField(write_only=True)
        Image=Base64ImageField()

        class Meta:
                model = AutoShow
                fields = ['pk','Name','Address','Image','StartAt','EndAt','EndAt','StartTime','EndTime','Posting','Phone','Latitude','Logitude','Category_Name','Category','MinPrice','MaxPrice','user']

class UserAutoShowAdminSerializer(serializers.ModelSerializer):
        password = serializers.CharField(style={"input_type": "password"},write_only=True)
        Image=Base64ImageField()

        class Meta:
                model = User
                fields = ['pk','Name','Image','Username','Phone','Address','password']

class ImageSerializer(serializers.ModelSerializer):
        Image=Base64ImageField()

        class Meta:
                model = CarImages
                fields = ['pk','Image']


class CarSerializer(serializers.ModelSerializer):
        carimages=ImageSerializer(many=True,source='carimages_set')


        class Meta:
                model = Car
                fields = ['pk','Name','Model','Color','Price','Phone','Miles','Gear','CreatedAt','ManufacturedAt','Status','Cylinder','Wheels','Chairs','Type','Description','CC','Sold','Latitude','Logitude','Furnaiture','Roof','Seller','Fuel','Number','Paint','Lock','Year','carimages',]
        # def create(self, validated_data):
        #         autoshowpk=self.context['request'].parser_context['kwargs']['autoshow']
        #         validated_data['AutoShow']=AutoShow(pk=autoshowpk)
        #         print(validated_data)
        #         CarImages_data=validated_data.pop("carimages_set")
        #         imagesCount=len(CarImages_data)
        #         if (not imagesCount<10):
        #                 raise serializers.ValidationError({"detail":"images is more than should"})
        #         if (not imagesCount>0):
        #                 raise serializers.ValidationError({"detail":"shoud send one image at less"})
               
                        
        #         try:
        #                 with transaction.atomic():

                        
        #                         car=super().create(validated_data)
        #                         print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
        #                         car_images_instances = [
        #                                 CarImages(Car=car, **image_data) for image_data in CarImages_data]
        #                         carimages=CarImages.objects.bulk_create(car_images_instances,batch_size=10)
        #                         print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
        #                         carx=car
        #                 carx.carimages_set.add(*carimages)
        #                 return carx
        #         except IntegrityError:
        #                 raise serializers.ValidationError({"detail":"Auto Show is not exist."})

class CarUpdateSerializer(serializers.ModelSerializer):
        

        class Meta:
                model = Car
                fields = ['pk','Name','Model','Color','Price','Phone','Miles','Gear','ManufacturedAt','Status','Cylinder','Wheels','Chairs','Type','Description','CC','Sold','Latitude','Logitude','Furnaiture','Roof','Seller','Fuel','Number','Paint','Lock','Year',]




class CarSubSerializer(serializers.ModelSerializer):
        carimages=ImageSerializer(many=True,source='carimages_set')


        class Meta:
                model = Car
                fields = ['pk','Name','Model','Color','Price','Gear','CreatedAt','carimages']

class AutoShowSubSerializer(serializers.ModelSerializer):
        Category_Name=serializers.CharField(read_only=True)

        class Meta:
                model = AutoShow
                fields = ['pk','Name','Address','Image','StartAt','StartTime','EndTime','Category_Name',]

class AutoShowSubSerializer2(serializers.ModelSerializer):

        class Meta:
                model = AutoShow
                fields = ['pk','Name','Address','Image','StartAt','StartTime','EndTime',]


class CategoryWithAutoShowSerializer(serializers.ModelSerializer):
        autoshow=AutoShowSubSerializer2(source='autoshow_set',many=True)
        class Meta:
                model = Category
                fields = ['Name','Description',"autoshow"]