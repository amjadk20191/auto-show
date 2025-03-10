# Generated by Django 4.2.9 on 2024-10-24 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Address', models.TextField()),
                ('Image', models.FileField(blank=True, null=True, upload_to='AutoShow/30784bd6-3528-4105-893e-a357d27f9ee1%Y%m%d')),
                ('MinPrice', models.FloatField(default=0)),
                ('MaxPrice', models.FloatField(default=999999999999999999999)),
                ('CreatedAt', models.DateField(auto_now_add=True)),
                ('StartAt', models.DateField()),
                ('EndAt', models.DateField()),
                ('StartTime', models.TimeField()),
                ('EndTime', models.TimeField()),
                ('Posting', models.PositiveIntegerField(blank=True, default=0)),
                ('Phone', models.CharField(max_length=30)),
                ('Latitude', models.FloatField()),
                ('Logitude', models.FloatField()),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.category')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Model', models.CharField(max_length=255)),
                ('Color', models.CharField(max_length=50)),
                ('Price', models.FloatField()),
                ('Phone', models.CharField(max_length=30)),
                ('Address', models.TextField()),
                ('Miles', models.FloatField(default=0)),
                ('Gear', models.CharField(max_length=255)),
                ('CreatedAt', models.DateField(auto_now_add=True)),
                ('ManufacturedAt', models.IntegerField()),
                ('Status', models.CharField(max_length=100)),
                ('Cylinder', models.CharField(max_length=100)),
                ('Wheels', models.IntegerField()),
                ('Chairs', models.IntegerField()),
                ('Type', models.CharField(max_length=100)),
                ('Description', models.TextField()),
                ('CC', models.FloatField()),
                ('Sold', models.BooleanField(default=False)),
                ('Latitude', models.FloatField()),
                ('Logitude', models.FloatField()),
                ('Furnaiture', models.TextField()),
                ('Roof', models.TextField()),
                ('Seller', models.TextField()),
                ('Fuel', models.TextField()),
                ('Number', models.TextField()),
                ('Paint', models.TextField()),
                ('Lock', models.TextField()),
                ('Views', models.BigIntegerField()),
                ('Year', models.IntegerField()),
                ('AutoShow', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auto_Show.autoshow')),
            ],
        ),
        migrations.CreateModel(
            name='CarImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.FileField(upload_to='Cars/366c9d23-52cb-4f74-8bfe-859f89e6aa7f%Y%m%d')),
                ('Car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auto_Show.car')),
            ],
        ),
    ]
