from django.contrib import admin

# Register your models here.

from .models import Products, Categories, ProductsCategories

admin.site.register(Products)
admin.site.register(Categories)
admin.site.register(ProductsCategories)
