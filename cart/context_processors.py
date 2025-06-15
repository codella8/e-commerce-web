from .models import Cart

def cart_items_count(request):
    cart_items_count = 0
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).prefetch_related('items').first()
        if cart:
            cart_items_count = cart.items.count()
    
    return {'cart_items_count': cart_items_count}
