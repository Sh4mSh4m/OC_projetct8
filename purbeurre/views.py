from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.views import generic

# Create your views here.
from .models import Products, UsersProducts
from django.contrib.auth.models import User

class IndexView(generic.ListView):
	template_name = 'purbeurre/index.html'
	context_object_name = 'latest_product'

	def get_queryset(self):
		return Products.objects.order_by('-name')[2000:2006]

class DetailView(generic.DetailView):
    model = Products
    template_name = 'purbeurre/detail.html'

def search(request):
    product_searched= request.GET.get('query')
    page = request.GET.get('page')
    products_list = Products.objects.filter(name__istartswith=product_searched).order_by('name')
    paginator = Paginator(products_list, 9)
    products = paginator.get_page(page)
    return render(request, 'purbeurre/search.html', {'products':products, 'product_searched': product_searched})


def substitute(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    substitutes = Products.objects.exclude(brands=product.brands).filter(main_category=product.main_category).filter(nutrition_grade__lte=product.nutrition_grade).order_by('nutrition_grade')[:6]
    return render(request, 'purbeurre/substitute.html', {'product':product, 'substitutes': substitutes})

def detail(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    return render(request, 'purbeurre/detail.html', {'product':product})

def my_products(request, user_id, product_id):
    user = get_object_or_404(User, pk=user_id)
    if product_id!=0:
        product_added = get_object_or_404(Products, pk=product_id)
        usersproducts = UsersProducts()
        usersproducts.user = user
        usersproducts.product = product_added
        already_added=False
        try:
            usersproducts.save()
        except:
            already_added=True
    else:
        already_added=False
        product_added=None
    #obtenir la liste des produits liés à l'utilisateur
    print("je vais choper les produits du user")
    products_list = Products.objects.filter(usersproducts__user_id=user_id).order_by('name')
    page = request.GET.get('page')
    paginator = Paginator(products_list, 9)
    products = paginator.get_page(page)
    return render(request, 'purbeurre/my_products.html', {'user': user, 
                                                          'product_added': product_added, 
                                                          'already_added': already_added,
                                                          'products': products})


def my_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'purbeurre/my_account.html', {'user': user})
