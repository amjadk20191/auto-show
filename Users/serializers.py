from rest_framework import serializers
from dashboard.models import Category
from Auto_Show.models import AutoShow, Car, CarImages



class CategorySerializer(serializers.ModelSerializer):
        class Meta:
                model = Category
                fields = '__all__'
    
    

class AutoShowListSerializer(serializers.ModelSerializer):
        class Meta:
            model = AutoShow
            fields = ['pk','Name','Address','Image','MinPrice','MaxPrice','StartAt','EndAt','StartTime','EndTime','Phone','Latitude','Logitude']



class ImageSerializer(serializers.ModelSerializer):

        class Meta:
                model = CarImages
                fields = ['pk','Image']




class CarListSerializer(serializers.ModelSerializer):
        carimages=ImageSerializer(many=True,source='carimages_set')

        class Meta:
            model = Car
            fields = ['pk','Name','Model','Color','Price','Gear','CreatedAt','carimages']


class CardetailsSerializer(serializers.ModelSerializer):
        carimages=ImageSerializer(many=True,source='carimages_set')

        class Meta:
            model = Car
            fields = ['pk','Name','Model','Color','Price','Phone','Miles','Gear','CreatedAt','ManufacturedAt','Status','Cylinder','Wheels','Chairs','Type','Description','CC','Latitude','Logitude','Furnaiture','Roof','Seller','Fuel','Number','Paint','Lock','Year','carimages']


class AutoShowSubSerializer2(serializers.ModelSerializer):

        class Meta:
                model = AutoShow
                fields = ['pk','Name','Address','Image','StartAt','StartTime','EndTime',]


class CategoryWithAutoShowSerializer(serializers.ModelSerializer):
        autoshow=AutoShowSubSerializer2(source='autoshow_set',many=True)
        class Meta:
                model = Category
                fields = ['Name','Description',"autoshow"]