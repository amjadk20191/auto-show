from django.contrib import admin

from .models import AutoShow, Car, CarImages


@admin.register(AutoShow)
class AutoShowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'Name',
        'Address',
        'Image',
        'MinPrice',
        'MaxPrice',
        'CreatedAt',
        'StartAt',
        'EndAt',
        'Posting',
        'Phone',
        'Latitude',
        'Logitude',
        'Category',
    )
    list_filter = ('CreatedAt', 'StartAt', 'EndAt', 'Category')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'Name',
        'Model',
        'Color',
        'Price',
        'Phone',
        'AutoShow',
        'Miles',
        'Gear',
        'CreatedAt',
        'ManufacturedAt',
        'Status',
        'Cylinder',
        'Wheels',
        'Chairs',
        'Type',
        'Description',
        'CC',
        'Sold',
        'Latitude',
        'Logitude',
    )
    list_filter = ('AutoShow', 'CreatedAt', 'Sold')


@admin.register(CarImages)
class CarImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'Car', 'Image')
    list_filter = ('Car',)