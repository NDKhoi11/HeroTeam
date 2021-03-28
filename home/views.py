from django.shortcuts import render, get_object_or_404
from django.views import View
from products.models import *
from django.http import JsonResponse
from django.template.loader import render_to_string

class Home(View):
    def get(self, request):
        category = Category.objects.all()
        products = Products.objects.all()
        isQuery = False

        #sent to home to use ajax to request filter-data process
        category_ajax = {
            "category_req": request.GET.get("category")
        }
        
        # filter category
        if request.GET.get("category"):
            products = products.filter(category__slug_category=request.GET.get("category"))
            isQuery = True
        
        # advance filter
        property = {
            "orderBy": request.GET.get("order-by"),
            "promotion": request.GET.get("promotion"),
            "available": request.GET.get("available"),
        }
        if property["orderBy"]:
            if property["orderBy"] == "price-up":
                products = products.order_by("price")
            if property["orderBy"] == "price-down":
                products = products.order_by("-price")
            if property["orderBy"] == "time":
                products = products.order_by("-created_at")
        else:
            products = products.order_by("-created_at")
                
        if property["available"]:
            if property["available"] == "all":
                products = products.filter(price__lte=1000000)
            if property["available"] == "yes":
                products = products.filter(price__gt=1000000, price__lte=5000000)
            if property["available"] == "no":
                products = products.filter(price__gt=5000000)

        if property["promotion"]:
            if property["promotion"] == "yes":
                products = products.filter(discount__gt=0)
            if property["promotion"] == "no":
                products = products.filter(discount=0)
                
        context = {
            "category": category,
            "products": products,
            "filter": property,
            "isQuery": isQuery,
            "category_ajax": category_ajax,
        }

        return render(request, "home.html", context)


class Search(View):
    def get(self, request):
        category = Category.objects.all()
        products = Products.objects.all()
        products = products.filter(name_product__icontains=request.GET.get("q", ""))
        
        # advance filter
        property = {
            "orderBy": request.GET.get("order-by"),
            "promotion": request.GET.get("promotion"),
            "available": request.GET.get("available"),
        }
        
        if property["orderBy"]:
            if property["orderBy"] == "price-up":
                products = products.order_by("price")
            if property["orderBy"] == "price-down":
                products = products.order_by("-price")
                
        if property["available"]:
            if property["available"] == "yes":
                products = products.filter(num_available__gt=0)
            if property["available"] == "no":
                products = products.filter(num_available=0)
                
        if property["promotion"]:
            if property["promotion"] == "yes":
                products = products.filter(discount__gt=0)
            if property["promotion"] == "no":
                products = products.filter(discount=0)
        context = {
            "category": category,
            "products": products,
            "filter": property,
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
    category = Category.objects.all()
    products = Products.objects.all()

    if category_req != 'None':
        products = products.filter(category__slug_category=category_req)


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
    else:
        products = products.order_by("-created_at")
                
    if property["available"]:
        if property["available"] == "all":
            products = products.filter(price__lte=1000000)
        if property["available"] == "yes":
            products = products.filter(price__gt=1000000, price__lte=5000000)
        if property["available"] == "no":
            products = products.filter(price__gt=5000000)

    if property["promotion"]:
        if property["promotion"] == "yes":
            products = products.filter(discount__gt=0)
        if property["promotion"] == "no":
            products = products.filter(discount=0)

    t = render_to_string('ajax/product-list.html',{'data':products})
    return JsonResponse({'data':t})
