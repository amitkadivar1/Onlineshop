from django.shortcuts import render, get_object_or_404
from .models import Category, Product,UserIpStore
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    UserIpStore.objects.create(userip=request.META['REMOTE_ADDR'])
    print(request.META['REMOTE_ADDR'])
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(Category__slug=category)
    return render(request, 'shop/product/list.html', {'cate gory': category, 'categories': categories, 'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
