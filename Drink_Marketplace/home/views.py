from django.shortcuts import render, get_object_or_404
from product.models import *
# Create your views here.
def Get_home(request):
    products = Product.objects.all()
    return render(request, 'home/home.html', {'products': products})# Truyền vào template


def product_detail(request, id):
    # Truy vấn sản phẩm dựa vào id
    product = get_object_or_404(Product, id=id)
    
    return render(request, 'home/product_detail.html', {'product': product})