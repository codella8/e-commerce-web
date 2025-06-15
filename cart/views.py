from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .cart import SessionCart
from app1.models import Product
from .forms import CartAddProductForm
from django.utils.translation import gettext as _
from django.utils.translation import get_language

def my_view(request):
    print("Current language:", get_language())

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart = SessionCart(request)
            cart.add(
                product=product,
                quantity=cd['quantity'],
                update_quantity=cd['update']
            )
            messages.success(request, _('محصول با موفقیت به سبد خرید اضافه شد'))
    return redirect('cart_detail')

def cart_detail(request):
    cart = SessionCart(request)
    items = list(cart)
    total_price = cart.get_total_price()
    
    for item in items:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            }
        )
    
    context = {
        'items': items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart_detail.html', context)

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = SessionCart(request)
    cart.remove(product)
    messages.success(request, _('محصول از سبد خرید حذف شد'))
    return redirect('cart_detail')

def update_quantity(request, product_id):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                messages.error(request, _('تعداد باید حداقل 1 باشد'))
                return redirect('cart_detail')
            
            product = get_object_or_404(Product, id=product_id)
            cart = SessionCart(request)
            cart.add(
                product=product,
                quantity=quantity,
                update_quantity=True 
            )
            messages.success(request, _('تعداد محصول با موفقیت به‌روزرسانی شد'))
        except ValueError:
            messages.error(request, _('لطفاً یک عدد معتبر وارد کنید'))
    
    return redirect('cart_detail')