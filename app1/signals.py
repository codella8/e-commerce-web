from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from app1.models import Profile
from payment.models import Order

# وقتی کاربر جدید ساخته میشه → پروفایل هم براش ساخته بشه
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# وقتی سفارش جدید ساخته میشه → ایمیل برای ادمین‌ها ارسال بشه
@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        # گرفتن ایمیل همه‌ی ادمین‌ها
        admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)

        # ارسال ایمیل به ادمین‌ها
        send_mail(
            subject="سفارش جدید ثبت شد",
            message=f"سفارش جدیدی با شماره {instance.id} ثبت شد.",
            from_email="no-reply@example.com",
            recipient_list=list(admin_emails),
            fail_silently=True,
        )
