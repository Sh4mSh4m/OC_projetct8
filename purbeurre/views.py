from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import Product

def index(request):
    latest_product = Product.objects.order_by('-name_product')[:3]
    context = {
        'latest_product': latest_product,
    }
    return render(request, 'purbeurre/index.html', context)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)