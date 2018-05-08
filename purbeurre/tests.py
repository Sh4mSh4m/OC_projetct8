from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.test import Client

from .models import Products, UsersProducts

    id = 20 
    url = "http://google.fr"
    name = "Kinder"
    description = "Kinder bueno plein de sucre"
    quantity = "80g"
    brands = "Ferrero"
    nutrition_grade = 15
    main_category = "Sucreries"
    productimageurl = "http://google.fr/image/20"
    productimagethumburl = "http://google.fr/image/thumb/20"


def create_product(**kwargs):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    return Products.objects.create(
                                   id = id,
                                   url = url,
                                   description = description,
                                   quantity = quantity,
                                   brands = brands,
                                   nutrition_grade= nutrition_grade,
                                   main_category = main_category,
                                   productimageurl = productimageurl,
                                   productimagethumburl = productimagethumburl
                                   )
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
        """
        product = create_product()
        response = self.client.get(reverse('purbeurre:detail', args=(product.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Voir la fiche du ")

    def test_search_no_login(self):
        """
        If no login, response OK
        """
        product = create_product()
        response = self.client.get('/purbeurre/search?query=kinder')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "kinder")

    def test_substitute_no_login(self):
        """
        If no login, response OK
        """
        product = create_product()
        response = self.client.get('/purbeurre/search?query=kinder')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "kinder")
