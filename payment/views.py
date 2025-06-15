from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import SessionCart 
from.forms import PaymentAddressForm
from .models import PaymentAddress
from .models import Order, OrderItem
from app1.models import  Profile
from django.utils.translation import gettext as _
from django.utils.translation import get_language

def my_view(request):
    print("Current language:", get_language())
    # ...

def payment_success(request):
    return render(request, 'payment/payment_success.html')

def checkout(request):
    cart = SessionCart(request)
    items = list(cart)
    total = cart.get_total_price()

    if request.user.is_authenticated:
        shipping_user = PaymentAddress.objects.filter(user=request.user).first()
        if request.method == 'POST':
            shipping_form = PaymentAddressForm(request.POST, instance=shipping_user)
            if shipping_form.is_valid():
                shipping_info = shipping_form.save(commit=False)
                shipping_info.user = request.user
                shipping_info.save()
                request.session['shipping_info_id'] = shipping_info.id 
                return redirect('confirm_order')
        else:
            shipping_form = PaymentAddressForm(instance=shipping_user)
    else:
        shipping_form = PaymentAddressForm(request.POST or None)
        if request.method == 'POST' and shipping_form.is_valid():
            shipping_info = shipping_form.save(commit=False)
            shipping_info.user = None  
            shipping_info.save()
            request.session['shipping_info_id'] = shipping_info.id
            return redirect('confirm_order')

    return render(request, 'payment/checkout.html', {
        'cart': cart,
        'items': items,
        'total_price': total,
        'shipping_form': shipping_form,
    })


def confirm_order(request):
    cart = SessionCart(request)
    items = list(cart)
    total_price = cart.get_total_price()

    shipping_info_id = request.session.get('shipping_info_id')
    shipping_info = PaymentAddress.objects.filter(id=shipping_info_id).first()

    if not shipping_info or not items:
        return redirect('checkout')

    return render(request, 'payment/confirm_order.html', {
        'items': items,
        'total_price': total_price,
        'shipping_info': shipping_info,
    })

def process_order(request):
    cart = SessionCart(request)
    items = list(cart)
    total = cart.get_total_price()

    if request.method == 'POST':
        shipping_info_id = request.session.get('shipping_info_id')
        shipping_info = PaymentAddress.objects.filter(id=shipping_info_id).first()

        if not shipping_info:
            messages.error(request, 'please full the form')
            return redirect('checkout')

        full_name = shipping_info.shipping_full_name
        email = shipping_info.shipping_email
        full_address = f"{shipping_info.shipping_address1}\n{shipping_info.shipping_address2}\n{shipping_info.shipping_city}\n{shipping_info.shipping_country}\n{shipping_info.shipping_zipcode}\n{shipping_info.shipping_state}"

        user = request.user if request.user.is_authenticated else None

        if not request.user.is_authenticated:
            messages.info(request, _('سفارش بدون ورود کاربر ثبت می‌شود.'))

        new_order = Order.objects.create(
        user=user,
        full_name=full_name,
        email=email,
        shipping_address=full_address,
        amount_paid=total,
        status='pending'
    )


        for item in items:
            OrderItem.objects.create(
                order=new_order,
                products=item['product_obj'],
                user=user,
                quantity=item['quantity'],
                price=item['price'],
            )

        cart.clear()

        if user:
            cu = Profile.objects.filter(user=user).first()
            if cu:
                cu.old_cart = ""
                cu.save()

        messages.success(request, _("سفارش با موفقیت ثبت شد."))
        return redirect('index')

    else:
        messages.error(request, _('درخواست نامعتبر بود.'))
        return redirect('index')
