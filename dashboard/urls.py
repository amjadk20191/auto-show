
from django.urls import path, include
from .views import CategoryViewset,carsubViewset, CategoryWithAutoShowViewset, AutoShowSubViewset, UserAdminViewset,UserAutoShowViewset, carViewset, AutoShowViewset, UserAutoShowAdminViewset, ImageViewset
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'category', CategoryViewset, basename="category")
router.register(r'user', UserAdminViewset, basename="user")
router.register(r'user-autoShow', UserAutoShowViewset, basename="user-autoShow")
router.register(r'autoShow', AutoShowViewset, basename="autoShow")
router.register(r'AutoShowAdmin', UserAutoShowAdminViewset, basename="AutoShowAdmin")
router.register(r'autoShow/(?P<autoshow>\d+)/car', carViewset, basename="car")
router.register(r'car/(?P<pkcar>\d+)/image', ImageViewset, basename="Image")
router.register(r'autoShow-sub', AutoShowSubViewset, basename="AutoShowSub")
router.register(r'autoShow/(?P<autoshow>\d+)/car-sub', carsubViewset, basename="carsub")
router.register(r'Category-autoShow', CategoryWithAutoShowViewset, basename="CA")



urlpatterns = [

    path('', include(router.urls)),

]
