from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.test import Client
from django.test.utils import setup_test_environment
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
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
    'nutrition_grade': 10,
    'main_category': "Sucreries",
    'productimageurl': "http://google.fr/image/21",
    'productimagethumburl': "http://google.fr/image/thumb/21",
    }

barre_cereales = {
    'id': 22,
    'url': "http://google.fr/barre_cereales",
    'name': "Barre cereales",
    'description': "Barre saine",
    'quantity': "80g",
    'brands': "Good food",
    'nutrition_grade': -7,
    'main_category': "Sucreries",
    'productimageurl': "http://google.fr/image/22",
    'productimagethumburl': "http://google.fr/image/thumb/22",
    }

def create_product(**kwargs):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    return Products.objects.create(**kwargs)


class TestAllViewsNoLogin(TestCase):
    def setUp(self):
        product = create_product(**kinder)
        product2 = create_product(**kinder_bueno)
        product3 = create_product(**barre_cereales)

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
        response = self.client.get('/purbeurre/20')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Voir la fiche du ")
        self.assertContains(response, "kinder") 

    def test_search_no_login(self):
        """
        If no login, response OK
        product name must be present in page. Along with product of same 
        main_category
        Includes link to login
        """
        response = self.client.get('/purbeurre/search?query=kinder')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kinder")
        self.assertContains(response, "bueno")
        self.assertNotContains(response, "cereales")

    def test_search_no_result_no_login(self):
        """
        If no login, response OK
        If searched product is not found, error message appears
        """
        response = self.client.get('/purbeurre/search?query=mlkjmlkj')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Désolé")


    def test_substitute_no_login(self):
        """
        If no login, response OK
        other product name must appear on page.
        Healthier option appears but not option of the same brands
        """
        response = self.client.get('/purbeurre/substitute/20')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kinder")
        self.assertNotContains(response, "bueno")
        self.assertContains(response, "cereales")
        self.assertContains(response, "Aller à la page d'authentification")

    def test_substitute_no_result_no_login(self):
        """
        If no login, response OK
        If no substitute, error message
        """
        response = self.client.get('/purbeurre/substitute/22')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Désolé")

    def test_accounts_no_login(self):
        """
        If no login, response OK
        Authentication fields available
        """
        response = self.client.get('/purbeurre/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Authentification")

    def test_sign_up(self):
        """
        If no login, response OK
        Authentication fields available
        """
        response = self.client.get(reverse('purbeurre:sign_up'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Créer votre compte")


class TestAllViewsLoggedIn(TestCase):
    def setUp(self):
        user = User.objects.create_user('billy', 'temporary@gmail.com', 'temporary')
        product = create_product(**kinder)
        product2 = create_product(**kinder_bueno)
        product3 = create_product(**barre_cereales)
        self.c = Client()
        self.c.login(username="billy", password="temporary")

    def test_substitute_logged_in(self):
        """
        If no login, response OK
        other product name must appear on page.
        Healthier option appears but not option of the same brands
        """
        response = self.c.get('/purbeurre/substitute/20')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kinder")
        self.assertNotContains(response, "bueno")
        self.assertContains(response, "cereales")
        self.assertContains(response, "Sauvegarder")

    def test_my_account(self):
        """
        my_acount page loads
        user email appears
        """
        response = self.c.get('/purbeurre/my_account/1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "temporary@gmail.com")

    def test_my_products(self):
        """
        my_products page loads
        default page invites user to use search bar to add products
        adding products is confirmed
        """
        response = self.c.get('/purbeurre/my_products/2/0')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Utilisez la barre de recherche")
        response = self.c.get('/purbeurre/my_products/2/22')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vous avez ajouté le produit")
        self.assertContains(response, "Barre cereales")



