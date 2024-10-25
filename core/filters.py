from django_filters.rest_framework import FilterSet
from Auto_Show.models import Car



class CarFilter(FilterSet):
    class Meta:
        model=Car
        fields={
            'Name':['exact'],
            'Color':['exact'],
            'Price':['lt'],
            'Status':['exact'],
            'Type':['exact'],
            'Address':['exact'],

        }
         