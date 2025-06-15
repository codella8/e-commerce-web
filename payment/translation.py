from modeltranslation.translator import register, TranslationOptions
from .models import PaymentAddress, Order

@register(PaymentAddress)
class PaymentAddressTranslationOptions(TranslationOptions):
    fields = (
        'shipping_full_name',
        'shipping_address1',
        'shipping_address2',
        'shipping_city',
        'shipping_state',
    )

@register(Order)
class OrderTranslationOptions(TranslationOptions):
    fields = (
        'full_name',
        'shipping_address',
    )