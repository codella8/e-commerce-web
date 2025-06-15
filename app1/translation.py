from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, Additionalproduct

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Additionalproduct)
class AdditionalProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')