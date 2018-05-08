from django.urls import path, include
from django.contrib import admin
from . import views


app_name = 'purbeurre'

urlpatterns = [
    # Index ex: /purbeurre/
    path('', views.index, name='index'),
    # Detail ex: /purbeurre/5/
    path('<int:product_id>/', views.detail, name='detail'),
    # Search ex: /purbeurre/search/banane%20de%20mer
    path('search', views.search, name='search'),
    # Substitute ex: /purbeurre/substitute/name
    path('substitute/<int:product_id>', views.substitute, name='substitute'),
    # Accounts ex: /purbeurre/accounts
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    # Admin ex: /purbeurre/back_admin/
    path('back_admin', admin.site.urls),
    # My_products ex: /purbeurre/my_products/2/0
    path('my_products/<int:user_id>/<int:product_id>', views.my_products, name='my_products'),
    # My_account ex: /purbeurre/my_products/2/0
    path('my_account/<int:user_id>', views.my_account, name='my_account'),
]