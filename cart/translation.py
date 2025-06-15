from modeltranslation.translator import register, TranslationOptions
from .models import Cart

@register(Cart)
class CartTranslationOptions(TranslationOptions):
    fields = ()