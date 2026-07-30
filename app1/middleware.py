from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin 

class AdminAccessMiddleware(MiddlewareMixin): 
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return redirect(f'{reverse("login")}?next={request.path}')
            if not request.user.is_staff:
                return redirect('index')
