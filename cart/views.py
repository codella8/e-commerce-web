from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .cart import SessionCart
from app1.models import Product
from .forms import CartAddProductForm
from django.utils.translation import gettext as _
from django.utils.translation import get_language

def my_view(request):
    print("Current language:", get_language()) #این خط زبان فعلی سایت رو چاپ می‌کنه،
 
def add_to_cart(request, product_id): # این خط تلاش می‌کنه یک شیء از مدل Product با id مشخص‌شده پیدا کنه
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = CartAddProductForm(request.POST) #شیئی از فرم CartAddProductForm می‌سازه و request.POST رو بهش میده تا داده‌ها رو پردازش کنه
        if form.is_valid(): #بررسی می‌کنه که داده‌های فرم معتبر هستن یا نه
            cd = form.cleaned_data # داده‌های تمیز و تاییدشده فرم رو در یک دیکشنری به نام cd ذخیره می‌کنه
            cart = SessionCart(request)
            cart.add( # متد ادد فراخوانی میشه و سخ پارامتر بهش داده میشه
                product=product, # شی محصول که باید به سبد خرید اضافه شود
                quantity=cd['quantity'], # تعداد مورد نظر از فرم
                update_quantity=cd['update'] # مقدار ها رو جایگزین ین اضافه میکنه برر اساس true/false
            )
            messages.success(request, _('محصول با موفقیت به سبد خرید اضافه شد')) # پیام موفقعیت آمیز
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