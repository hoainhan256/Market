# card/views.py

from django.shortcuts import get_object_or_404, redirect, render
from product.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Lấy hoặc tạo giỏ hàng cho user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Lấy hoặc tạo item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('card:cart_detail')


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = sum(item.total_price() for item in items)
    return render(request, 'card/cart.html', {'cart': cart, 'items': items, 'total': total})

