from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.views import generic

# Create your views here.
from .models import Products, UsersProducts
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth import login, authenticate



def index(request):
    return render(request, 'purbeurre/index.html')

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

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/purbeurre/')
    else:
        form = SignUpForm()
    return render(request, 'purbeurre/sign_up.html', {'form': form})

