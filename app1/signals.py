from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from payment.models import Order
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
@receiver(post_save, sender=Order,)
def order_created(sender, instance, created, **kwargs):
    if created:
        admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
        send_mail(
            subject="سفارش جدید ثبت شد",
            message=f"سفارش جدیدی با شماره {instance.id} ثبت شد.",
            from_email="no-reply@example.com",
            recipient_list=list(admin_emails),
            fail_silently=True,
        )
