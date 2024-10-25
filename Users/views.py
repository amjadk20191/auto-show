from rest_framework import generics,viewsets,views
from dashboard.models import Category
from .serializers import CategoryWithAutoShowSerializer, CardetailsSerializer, CarListSerializer, CategorySerializer, AutoShowListSerializer
from Auto_Show.models import AutoShow, Car
from django_filters.rest_framework import DjangoFilterBackend
from core.filters import CarFilter
from rest_framework.filters import SearchFilter
from django.db.models import Prefetch

from core.pagination import DefaultPagination
class CategoryList(generics.ListAPIView):
    
    serializer_class = CategorySerializer
    queryset=Category.objects.all()
    # pagination_class=DefaultPagination



class AutoShowList(generics.ListAPIView):
    
    serializer_class = AutoShowListSerializer
    # pagination_class=DefaultPagination

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pkC')
        self.queryset =AutoShow.objects.only('Name','Address','Image','MinPrice','MaxPrice','StartAt','EndAt','StartTime','EndTime','Phone','Latitude','Logitude').filter(Category=pk)
        return super().get_queryset()
    


class CarList(generics.ListAPIView):
    
    serializer_class = CarListSerializer
    pagination_class=DefaultPagination

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pkAS')
        self.queryset =Car.objects.prefetch_related("carimages_set").only('Name','Model','Color','Price','Gear','CreatedAt').filter(AutoShow=pk,Sold=False)
        return super().get_queryset()
    

class CarDetails(generics.RetrieveAPIView):
    
    serializer_class = CardetailsSerializer

    def get_queryset(self, *args, **kwargs):
        # pk = self.kwargs.get('pk')
        self.queryset =Car.objects.prefetch_related("carimages_set").only(

            'pk','Name','Model','Color','Price','Phone','Miles','Gear','CreatedAt','ManufacturedAt','Status','Cylinder','Wheels','Chairs','Type','Description','CC','Latitude','Logitude','carimages'
            ,'Furnaiture','Roof','Seller','Fuel','Number','Paint','Lock','Year'
        ).filter(Sold=False)
        return super().get_queryset()
    


class CarSearchList(generics.ListAPIView):
    
    serializer_class = CarListSerializer
    pagination_class=DefaultPagination

    queryset=Car.objects.prefetch_related("carimages_set").only('Name','Model','Color','Price','Gear','CreatedAt').filter(Sold=False)
    filter_backends=[DjangoFilterBackend,SearchFilter]
    filterset_class=CarFilter
    search_fields=['Model','Description']
     

class CategoryWithAutoShowViewset(viewsets.ModelViewSet):
    
    http_method_names=['get',]
    serializer_class = CategoryWithAutoShowSerializer
    autoshow_queryset = AutoShow.objects.only('pk','Name','Address','Image','StartAt','StartTime','EndTime','Category')

    queryset=Category.objects.prefetch_related(
         Prefetch('autoshow_set', queryset=autoshow_queryset)
    ).only("Name","Description").all()