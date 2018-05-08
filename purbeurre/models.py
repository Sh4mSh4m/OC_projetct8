# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings


class Categories(models.Model):
    id = models.IntegerField(primary_key=True)
    name_category = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Products(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    brands = models.CharField(max_length=100, blank=True, null=True)
    nutrition_grade = models.FloatField(blank=True, null=True)
    main_category = models.CharField(max_length=100, blank=True, null=True)
    productimageurl = models.CharField(db_column='productImageUrl', max_length=200, blank=True, null=True)  # Field name made lowercase.
    productimagethumburl = models.CharField(db_column='productImageThumbUrl', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'products'
        unique_together = (('name', 'description', 'quantity'),)


class ProductsCategories(models.Model):
    product = models.ForeignKey(Products, models.DO_NOTHING)
    category = models.ForeignKey(Categories, models.DO_NOTHING)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'products_categories'
        unique_together = (('product', 'category'),)


class UsersProducts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.OneToOneField(Products, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'users_products'
        unique_together = (('user', 'product'),)
