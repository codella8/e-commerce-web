from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from modeltranslation.admin import TranslationAdmin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug') 
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} 

@admin.register(models.Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['name', 'price', 'category', 'is_sale']

@admin.register(models.Additionalproduct)
class AdditionalProductAdmin(TranslationAdmin):
    list_display = ['name', 'price', 'category', 'is_sale']

@admin.register(models.ProductMessage)
class ProductMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'product', 'created_at']

@admin.register(models.AdditionalProductMessage)
class AdditionalProductMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'product', 'created_at']

class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False

class CustomUserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
