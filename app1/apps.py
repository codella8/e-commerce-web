from django.apps import AppConfig

class App1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app1'
    
    def ready(self): # این متد برای لود کردن فایل های سیگنال ها به کار میرود
        import app1.signals # برای دریافت سیگنال ها از signals.py
        import app1.translation # برا ی تنظیمات چندربانه 
