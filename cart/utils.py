from cart.models import Cart

def migrate_session_cart_to_user(request, user):
    session_key = request.session.session_key
    session_cart = Cart.objects.filter(session_key=session_key, user=None).first()

    if session_cart:
        user_cart, created = Cart.objects.get_or_create(user=user)

        for item in session_cart.items.all():
            existing_item = user_cart.items.filter(product=item.product).first()
            if existing_item:
                existing_item.quantity += item.quantity
                existing_item.save()
            else:
                item.cart = user_cart
                item.save()

        session_cart.delete()