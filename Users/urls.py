from .views import CategoryWithAutoShowViewset, CarDetails, CategoryList, AutoShowList, CarList, CarSearchList
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'Category-autoShow', CategoryWithAutoShowViewset, basename="CategoryWithAutoShow")



urlpatterns = [
    path('category/', CategoryList.as_view(), name="category"),
    path('category/<int:pkC>/AutoShow/', AutoShowList.as_view(), name="AutoShow"),
    path('AutoShow/<int:pkAS>/cars/', CarList.as_view(), name="CarList"),
    path('car-detail/<int:pk>/', CarDetails.as_view(), name="CarDetails"),
    path('car-search/', CarSearchList.as_view(), name="CarSearchDetails"),

    path('', include(router.urls)),

]
