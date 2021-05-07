from django.shortcuts import render, get_object_or_404
from django.views import View
from products.models import *
from django.http import JsonResponse
from django.template.loader import render_to_string

class Home(View):
    def get(self, request):
        category = Category.objects.all()
        context = {
            "category": category,
        }

        return render(request, "home.html", context)

class DetailProduct(View):
    def get(self, request, slug):
        product = get_object_or_404(Products, slug_product=slug)
        context = {
            "product": product,
        }
        return render(request, "products/detail-product.html", context)

def filter_data(request):
    orderby=request.GET.get('order-by')
    promotions=request.GET.get('promotion')
    availables=request.GET.get('available')
    category_req = request.GET.get('category_req')
    search_req = request.GET.get('search_req')
    products = Products.objects.all()

    #check exits of request
    if category_req != 'None' and category_req:
        products = products.filter(category__slug_category=category_req)
    if search_req != 'None' and search_req:
        products = products.filter(name_product__icontains=search_req)

    property = {
        "orderBy": orderby,
        "promotion": promotions,   
        "available": availables,
    }

    if property["orderBy"]:
        if property["orderBy"] == "price-up":
            products = products.order_by("price")
        if property["orderBy"] == "price-down":
            products = products.order_by("-price")
        if property["orderBy"] == "time":
            products = products.order_by("-created_at")
            
    if property["available"]:
        if property["available"] == "down1m":
            products = products.filter(price__lte=1000000)
        if property["available"] == "from1mto5m":
            products = products.filter(price__gt=1000000, price__lte=5000000)
        if property["available"] == "up5m":
            products = products.filter(price__gt=5000000)
        if property["available"] == "all":
            products = products

    if property["promotion"]:
        if property["promotion"] == "yes":
            products = products.filter(discount__gt=0)
        if property["promotion"] == "no":
            products = products.filter(discount=0)
        if property["promotion"] == "all":
            products = products

    t = render_to_string('ajax/product-list.html',{'products':products})
    return JsonResponse({'data':t})
