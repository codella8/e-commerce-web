from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin 

#این میانه‌افزار به‌طور مؤثر از دسترسی کاربران غیر ادمین به بخش ادمین جلوگیری می‌کند
class AdminAccessMiddleware(MiddlewareMixin): 
    def process_view(self, request, view_func, view_args, view_kwargs):
        # بررسی اینکه آیا درخواست مربوط به بخش ادمین است
        if request.path.startswith('/admin/'):
            # اگر کاربر وارد نشده باشد، به صفحه ورود هدایت می‌شود
            if not request.user.is_authenticated:
                return redirect(f'{reverse("login")}?next={request.path}')
            # اگر کاربر ادمین نباشد، به صفحه اصلی هدایت می‌شود
            if not request.user.is_staff:
                return redirect('index')
