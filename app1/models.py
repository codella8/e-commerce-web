from django.db import models
from django.core.validators import MinValueValidator , MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
  
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=25, blank=True)
    address1 = models.CharField(max_length=250, blank=True)
    address2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=25, blank=True)
    zipcode = models.CharField(max_length=25, blank=True)
    country = models.CharField(max_length=25, default='IRAN')
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username 

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(blank=True, null=True) 
    
    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=40, verbose_name="نام محصول")
    description = models.CharField(max_length=500, verbose_name="توضیحات", default='', blank=True, null=True)
    price = models.DecimalField(verbose_name="قیمت",default=0, decimal_places=0, max_digits=14)
    category = models.ForeignKey('Category', verbose_name="دسته بندی", on_delete=models.CASCADE, default=1)
    picture = models.ImageField(upload_to='upload/product', null=True, blank=True)
    star = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    is_sale = models.BooleanField(verbose_name="تخفیف",default=False) 
    sale_price = models.DecimalField(verbose_name="قیمت بعد از تخفیف",default=0, decimal_places=0, max_digits=14) 
    
    def __str__(self): #نمایش نام محصول به جای شیء در پنل ادمین
        return self.name
    
    class Meta: #تعریف نام فارسی مدل برای پنل مدیریت
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def get_final_price(self): #برگرداندن قیمت نهایی براساس تخفیف
        if self.is_sale:
            return self.sale_price
        return self.price
    
    #جلوگیری از ذخیره محصولاتی که تخفیف‌شان اشتباه تنظیم شده 
    # (یعنی تخفیف ندارند ولی is_sale = True خورده، یا تخفیف‌شان بیشتر از قیمت اصلی است).
    def save(self, *args, **kwargs):
        if self.is_sale and self.sale_price >= self.price:
            raise ValidationError("قیمت تخفیف باید کمتر از قیمت اصلی باشد")
        super().save(*args, **kwargs)
    
class Additionalproduct(models.Model):
    name = models.CharField(max_length=40, verbose_name="نام محصول")
    description = models.CharField(max_length=500, verbose_name="توضیحات", default='', blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name="دسته بندی", on_delete=models.CASCADE, default=1)
    picture = models.ImageField(upload_to='upload/More_product')
    price = models.DecimalField(verbose_name="قیمت",default=0, decimal_places=0, max_digits=14)
    star = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    is_sale = models.BooleanField(verbose_name="قیمت تخفیف",default=False)
    sale_price = models.DecimalField(verbose_name="قیمت بعد از تخفیف",default=0, decimal_places=0, max_digits=14)
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات بیشتر"
    
    def __str__(self):
        return self.name
    
class ProductMessage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='messages')
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True) #تاریخ و زمان ایجاد پیام. به‌طور خودکار هنگام ایجاد ذخیره می‌شود
    
    class Meta:
        verbose_name = "پیام محصول"
        verbose_name_plural = "پیام‌های محصولات"

    def __str__(self):
        return _("پیام از %(name)s برای %(product)s") % {
            'name': self.name,
            'product': self.product.name
        }
    
class AdditionalProductMessage(models.Model):
    product = models.ForeignKey('Additionalproduct', on_delete=models.CASCADE, related_name='messages')
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "پیام محصول"
        verbose_name_plural = "پیام‌های محصولات بیشتر"

    def __str__(self):
        return _("پیام از %(name)s برای %(product)s") % {
            'name': self.name,
            'product': self.product.name
        }
