from django.urls import path
from . import views
from django.http import JsonResponse
from django.template.loader import render_to_string

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("detail/<str:slug>", views.DetailProduct.as_view(), name="detail"),
    path("search/", views.Search.as_view(), name="search"),
    path('filter-data',views.filter_data,name='filter_data'),
]