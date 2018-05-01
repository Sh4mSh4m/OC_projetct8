from django.urls import path

from . import views


app_name = 'purbeurre'

urlpatterns = [
    # ex: /purbeurre/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /purbeurre/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /purbeurre/search/banane%20de%20mer
    path('search/<str:product_searched>', views.search, name='search'),
    # ex: /polls/5/results/
    path('substitute/<str:product_searched>', views.substitute, name='substitute'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]