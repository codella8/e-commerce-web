from django.db import models
from django.contrib.auth.models import User
from app1.models import Product
from django_jalali.db import models as jmodels
import jdatetime
from django.utils.translation import gettext_lazy as _


class PaymentAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=250)
    shipping_email = models.CharField(max_length=300)
    shipping_phone = models.CharField(max_length=25, blank=True)
    shipping_address1 = models.CharField(max_length=250, blank=True)
    shipping_address2 = models.CharField(max_length=250, blank=True, null=True)
    shipping_city = models.CharField(max_length=25, blank=True)
    shipping_state = models.CharField(max_length=25, blank=True)
    shipping_zipcode = models.CharField(max_length=25, blank=True)
    shipping_country = models.CharField(max_length=25, blank=True, default='IRAN')

    class Meta:
        verbose_name = _('آدرس پرداخت')
        verbose_name_plural = _('آدرس‌های پرداخت')

    def __str__(self):
        return _('فرم آدرس پرداخت: {name}').format(name=self.shipping_full_name)

class Order(models.Model):
    STATUS_ORDER = [
    ('pending', 'در انتظار پرداخت'),
    ('processing', 'در حال پردازش'),
    ('shipped', 'ارسال شده به پست'),
    ('delivered', 'تحویل داده شده'),
]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=300)
    shipping_address = models.TextField(max_length=400)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=14) 
    date_ordered = jmodels.jDateTimeField(auto_now_add=True)
    last_update = jmodels.jDateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_ORDER, default='pending')
    
    class Meta:
        verbose_name = _('سفارش')
        verbose_name_plural = _('سفارشات')
    
    def save(self, *args, **kwargs):
        old_status = None

        if self.pk:
            old = Order.objects.filter(pk=self.pk).first()
            if old:
                old_status = old.status
        if old_status != self.status:
            self.last_update = jdatetime.datetime.now()

        super().save(*args, **kwargs)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=14)
    
    class Meta:
        verbose_name = _('آیتم های سفارش')

    def __str__(self):
        if self.user is not None:
            return _('آیتم سفارش - {product} - برای {user}').format(
                product=self.products,
                user=self.user
            )
        return _('آیتم سفارش - {product} - برای سفارش {order}').format(
            product=self.products,
            order=self.order
        )
