from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem

@receiver(user_logged_in)
def transfer_session_cart_to_user(sender, request, user, **kwargs):
    session_key = request.session.session_key
    session_cart = Cart.objects.filter(session_key=session_key, user=None).first()

    if not session_cart:
        return

    user_cart, created = Cart.objects.get_or_create(user=user)

    for item in session_cart.items.all():
        existing_item = CartItem.objects.filter(cart=user_cart, product=item.product).first()
        if existing_item:
            existing_item.quantity += item.quantity
            existing_item.save()
        else:
            CartItem.objects.create(cart=user_cart, product=item.product, quantity=item.quantity)
    session_cart.items.all().delete()
    session_cart.delete()
