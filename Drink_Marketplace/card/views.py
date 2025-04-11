# card/views.py

from django.shortcuts import get_object_or_404, redirect, render
from product.models import Product
from .models import Cart, CartItem
from product.models import Order, OrderItem
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
def checkout(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        # Trường hợp không có giỏ
        return redirect('card:cart_detail')  # hoặc render lỗi

    cart_items = cart.items.all()

    if not cart_items:
        return redirect('card:cart_detail')  # Không có gì để thanh toán

    # Bước 1: Tạo đơn hàng
    order = Order.objects.create(user=user)

    # Bước 2: Tạo các OrderItem từ các CartItem
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price  # lưu lại giá lúc thanh toán
        )

    # Bước 3: Xoá sạch CartItems
    cart.items.all().delete()

    # Optional: hoặc xóa luôn cart nếu bạn muốn
    # cart.delete()

    # Bước 4: Chuyển hướng hoặc hiển thị thông báo
    return redirect('card:history')
@login_required
def purchase_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'card/history.html', {'orders': orders})
