from django.db import models

# Create your models here.
class Product(models.Model):
    name_product = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    quantity = models.CharField(max_length=20)
    nutrition = models.CharField(max_length=2)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    code = models.IntegerField()#INT

    def __str__(self):
        return self.name_product

class Category(models.Model):
	"""
    #name_category_fr VARCHAR(200) NOT NULL,\
    #name_category VARCHAR(200) NOT NULL,\
    #nb_products INT UNSIGNED,\
    """
