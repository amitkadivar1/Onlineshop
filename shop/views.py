from django.shortcuts import render, get_object_or_404
from .models import Category, Product,UserIpStore
from cart.forms import CartAddProductForm
import requests
from decouple import config

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    ipstackapikey=config('IPSTACKAPI')
    googlemapapikey=config('GOOGLEMAPAPIKEY')
    
    response = requests.get('http://api.ipstack.com/check?access_key={}'.format(ipstackapikey))
    geodata=response.json()
    userip=geodata['ip']
    countryname=geodata['country_name'] 
    regionname=geodata['region_name']
    city=geodata['city'] 
    latitude=geodata['latitude'] 
    longitude=geodata['longitude'] 
    UserIpStore.objects.create(userip=userip,countryname=countryname,regionname=regionname, city=city,latitude=latitude,longitude=longitude)
    print(request.META.get('HTTP_X_FORWARDED_FOR', ''))
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(Category__slug=category)
    return render(request, 'shop/product/list.html', {'cate gory': category, 'categories': categories, 'products': products,'latitude':latitude,'longitude':longitude,'mapapikey':googlemapapikey})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
