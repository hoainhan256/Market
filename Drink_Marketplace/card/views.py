# views.py trong app cart
from django.shortcuts import render, redirect
from django.http import JsonResponse
from product.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
import json

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_name = data.get('name')
        product_price = data.get('price')
        product_img = data.get('img')

        # Kiểm tra xem sản phẩm có trong cơ sở dữ liệu không
        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sản phẩm không tồn tại.'})

        # Kiểm tra xem người dùng đã có giỏ hàng chưa
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            # Nếu sản phẩm đã có trong giỏ hàng, tăng số lượng lên
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Request method must be POST'})



@login_required
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    
    # Tính tổng giá trị của từng sản phẩm trong giỏ hàng
    cart_items = cart.items.all()
    total_price = sum(item.total_price() for item in cart_items)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'card/cart.html', context)

