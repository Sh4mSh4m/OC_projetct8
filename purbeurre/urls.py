from django.urls import path

from . import views


app_name = 'purbeurre'

urlpatterns = [
    # ex: /purbeurre/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /purbeurre/5/
    path('<int:product_id>/', views.detail, name='detail'),
    # ex: /purbeurre/search/banane%20de%20mer
    path('search', views.search, name='search'),
    # ex: /purbeurre/substitute/name
    path('substitute/<int:product_id>', views.substitute, name='substitute'),
]