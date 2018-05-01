from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views import generic

# Create your views here.
from .models import Products	

class IndexView(generic.ListView):
	template_name = 'purbeurre/index.html'
	context_object_name = 'latest_product'

	def get_queryset(self):
		return Products.objects.order_by('-name')[2000:2006]

class DetailView(generic.DetailView):
    model = Products
    template_name = 'purbeurre/detail.html'

def detail(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    return render(request, 'purbeurre/detail.html', {'product':product})

def search(request):
    product_searched= request.GET.get('query')
    products = Products.objects.filter(name__istartswith=product_searched)[:9]
    return render(request, 'purbeurre/search.html', {'products':products, 'product_searched': product_searched})

def substitute(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    substitutes = Products.objects.exclude(brands=product.brands).filter(main_category=product.main_category).filter(nutrition_grade__gte=product.nutrition_grade).order_by('-nutrition_grade')[:6]
    return render(request, 'purbeurre/substitute.html', {'product':product, 'substitutes': substitutes})

