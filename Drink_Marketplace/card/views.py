# card/views.py

from django.shortcuts import get_object_or_404, redirect, render
from product.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Kiểm tra nếu người dùng đã có giỏ hàng, nếu chưa thì tạo mới
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Kiểm tra nếu sản phẩm đã có trong giỏ
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # Nếu sản phẩm đã có trong giỏ, tăng số lượng
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    # Debug: In giỏ hàng sau khi thêm sản phẩm
    print("Giỏ hàng sau khi thêm sản phẩm: ", cart.items.all())

    # Sau khi thêm vào giỏ, chuyển hướng lại trang giỏ hàng
    return redirect('home')
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()  # Đây là nơi lấy ra tất cả các item trong giỏ hàng
    total = sum(item.total_price() for item in items)

    # Render lại trang giỏ hàng với tất cả các sản phẩm
    return render(request, 'card/cart.html', {'items': items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    try:
        # Tìm sản phẩm cần xoá
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()

        # Sau khi xoá sản phẩm, kiểm tra lại tổng số lượng và tổng tiền
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
        total = sum(item.total_price() for item in items)
        if not items:
            # Nếu giỏ hàng trống
            message = "Giỏ hàng của bạn đã trống."
            return render(request, 'card/cart.html', {'items': items, 'total': total, 'message': message})
        
    except CartItem.DoesNotExist:
        return redirect('home')

    # Quay lại trang giỏ hàng sau khi xóa
    return redirect('card:cart_detail')
