from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.test import Client

from .models import Products, UsersProducts

kinder = {
    'id': 20,
    'url': "http://google.fr/kinder",
    'name': "Kinder",
    'description': "Kinder le truc plein de sucre",
    'quantity': "80g",
    'brands': "Ferrero",
    'nutrition_grade': 15,
    'main_category': "Sucreries",
    'productimageurl': "http://google.fr/image/20",
    'productimagethumburl': "http://google.fr/image/thumb/20",
    }

kinder_bueno = {
    'id': 21,
    'url': "http://google.fr/kinder_bueno",
    'name': "Kinder bueno",
    'description': "Kinder bueno plein de sucre",
    'quantity': "80g",
    'brands': "Ferrero",
    'nutrition_grade': 0,
    'main_category': "Sucreries",
    'productimageurl': "http://google.fr/image/21",
    'productimagethumburl': "http://google.fr/image/thumb/21",
    }


def create_product(**kwargs):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    return Products.objects.create(**kwargs)

class TestAllViewsNoLogin(TestCase):
    def test_index_no_login(self):
        """
        If no login, response OK.
        """
        response = self.client.get(reverse('purbeurre:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras")

    def test_detail_no_login(self):
        """
        If no login, response OK
        Contains text of the detail.html page.detail
        Contains name of the product
        """
        product = create_product(**kinder)
        response = self.client.get(reverse('purbeurre:detail', args=(product.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Voir la fiche du ")
        self.assertContains(response, "kinder") 

    def test_search_no_login(self):
        """
        If no login, response OK
        product name must be present in page.
        """
        product = create_product(**kinder)
        response = self.client.get('/purbeurre/search?query=kinder')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kinder")

    def test_substitute_no_login(self):
        """
        If no login, response OK
        other product name must appear on page.
        """
        product = create_product(**kinder)
        product2 = create_product(**kinder_bueno)
        response = self.client.get(reverse('purbeurre:substitute', args=(product.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kinder")
        self.assertContains(response, "Kinder bueno")
