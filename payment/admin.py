# payment/admin.py
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import PaymentAddress, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['products', 'quantity', 'price']
    readonly_fields = ['products', 'quantity', 'price']

@admin.register(PaymentAddress)
class PaymentAddressAdmin(TranslationAdmin):
    list_display = ['shipping_full_name', 'user', 'shipping_city']
    search_fields = ['shipping_full_name', 'user__username']

@admin.register(Order)
class OrderAdmin(TranslationAdmin):
    list_display = ['full_name', 'email', 'amount_paid', 'status']
    list_filter = ['status', 'date_ordered']
    search_fields = ['full_name', 'email']
    readonly_fields = ['date_ordered', 'last_update']
    inlines = [OrderItemInline]

admin.site.register(OrderItem)