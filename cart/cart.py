from cart.models import Cart, CartItem

class SessionCart:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user

        if not self.session.session_key:
            self.session.save()

        if self.user.is_authenticated:
            self.cart = Cart.objects.filter(user=self.user).first()
            if not self.cart:
                self.cart = Cart.objects.create(user=self.user)
        else:
            self.cart = Cart.objects.filter(session_key=self.session.session_key, user=None).first()
            if not self.cart:
                self.cart = Cart.objects.create(session_key=self.session.session_key, user=None)

        self.session['cart_id'] = self.cart.id

    def __iter__(self):
        items = self.cart.items.select_related('product')
        for item in items:
            yield {
                'id': item.id,
                'product': item.product,
                'product_obj': item.product,  # برای سازگاری با تمپلیت‌های موجود
                'quantity': item.quantity,
                'price': item.get_unit_price(),  # از متد جدید CartItem استفاده می‌کند
                'total_price': item.get_total_price()  # از متد جدید CartItem استفاده می‌کند
            }

    def __len__(self):
        return self.cart.items.count()

    def add(self, product, quantity=1, update_quantity=False):
        item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            if update_quantity:
                item.quantity = quantity
            else:
                item.quantity += quantity
            item.save()

    def remove(self, product):
        self.cart.items.filter(product=product).delete()

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cart.items.all())

    def clear(self):
        self.cart.items.all().delete()
        if 'cart_id' in self.session:
            del self.session['cart_id']
            self.session.modified = True
