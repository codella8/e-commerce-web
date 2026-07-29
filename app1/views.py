# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from . models import Product, Additionalproduct, ProductMessage, AdditionalProductMessage, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from cart.utils import migrate_session_cart_to_user
from django.contrib.auth.models import User
from .forms import ProductMessageForm
from .forms import AdditionalProductMessageForm
from . forms import SignUpForm, UserUpdateForm, UpdatePasswordForm, UpdateUserInfo
from django.db.models import Q
from payment.models import Order, OrderItem
# for translation
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import get_language

def my_view(request):
    print("Current language:", get_language())

def admin_only(user):
    return user.is_staff 

@user_passes_test(admin_only) #فقط به ادمین‌ها اجازه ورود می‌دهد
def admin_panel(request):
    return redirect('admin:index') #ارسال کاربر به داشبورد پنل مدیریت

def home(request):    
    context = {
        'welcome_message': _("Hello Welcome!")
    }
    return render(request, 'index.html', context)

def user_orders(request):
    if request.user.is_authenticated:
        #فقط سفارش‌های تحویل‌شده
        delivered_orders = Order.objects.filter(user=request.user, status='Delivered')
        #سفارش‌های در حال انجام یا تحویل‌نشده (مثل Pending، Processing، Shipped و...)
        current_orders = Order.objects.filter(user=request.user).exclude(status='Delivered')

        context = {
            'delivered_orders': delivered_orders,
            'current_orders': current_orders,
        }

        return render(request, 'orders.html', context)

    
    else:
        messages.error(request, 'not avilable!')
        return redirect('index')
    
#هدف از این ویو : نمایش جزئیات یک سفارش
#نیاز به احراز هویت – فیلتر سفارش با شناسه – بهتره بررسی شود که سفارش متعلق به خود کاربر است       
def order_details(request, pk):
    if request.user.is_authenticated:
        #برای جلوگیری از دیدن سفارش‌های دیگران
        order = get_object_or_404(Order, id=pk, user=request.user) #سفارش خاص با شناسه pk (Primary Key) رو از دیتابیس می‌گیره.
        items = OrderItem.objects.filter(order=pk) #سفارش‌های داخل سفارش
        # همه آیتم‌هایی که به این سفارش تعلق دارن رو از جدول OrderItem می‌گیره.
        # یعنی همه محصولاتی که در سفارش بودن.
        context = {
            'order': order,
            'items': items,
        }
        
        return render(request, 'order_details.html', context)
    
    else:
        messages.error(request, 'not avilable!')
        return redirect('index')

# هدف از این ویو : جستجوی محصولات
#استفاده از Q و icontains – 
# جستجوی هوشمند با چند شرط

def search(request):
    searched = request.POST.get('searched') #کلمه‌ای که کاربر در فرم جستجو تایپ کرده رو از فرم می‌گیره.
    products = Product.objects.filter(
        Q(name__icontains=searched) | Q(description__icontains=searched)
    ) if searched else []
    return render(request, 'search.html', { #مقدار جستجو شده و لیست نتایج رو به قالب می‌فرسته.
        'searched': searched,
        'products': products
    })


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def logout_user(request):
    logout(request)
    messages.success(request, _('با موفقیت خارج شدید'))
    return redirect('index')

# 
def login_user(request): # تعریف ویوی ورود
    if request.user.is_authenticated:
        messages.info(request, _("شما قبلاً وارد شده‌اید."))
        return redirect("index") # اینکار باعث جلوگیری از ورود دوباره‌ی کاربران وارد شده می‌شود

    if request.method == "POST": # گرفتن داده ها
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password) # بررسی اعتبار با authenticated

        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', 'index') #اگر کاربر از یک صفحه خاص به login هدایت شده بود next را برمیگرداند
            
            if '/admin/' in next_page and not user.is_staff:
                messages.error(request, _("شما دسترسی به پنل مدیریت ندارید"))
                return redirect('index') # محافظت از صفحه ادمین
                
            return redirect(next_page)
        else:
            messages.error(request, _("نام کاربری یا رمز عبور اشتباه است"))
    
    return render(request, 'login.html')
def signup_user(request):
    if request.method == "POST": # بررسی درخواست از نوع post
        form = SignUpForm(request.POST)
        if form.is_valid(): #فرم وارد شده را اعتبارسنجی می‌کنیم
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists(): #بررسی وجود نام کاربری و ایمیل
                form.add_error('username', _("این نام کاربری قبلاً ثبت شده است."))
            elif User.objects.filter(email=email).exists():
                form.add_error('email', _("این ایمیل قبلاً ثبت شده است."))
            else:
                user = form.save()
                Profile.objects.get_or_create(user=user) # ایجاد پروفایل کاربر 
                #get_or_create() بررسی میکند که آیا پروفایل برای این کاربر وجود دارد یا خیر
                login(request, user) # ورود کاربر به حساب
                migrate_session_cart_to_user(request, user) #مهاجرت سبد خرید به حساب کاربر 
                messages.success(request, _("اکانت شما ساخته شد."))
                return redirect("index")

        messages.error(request, _("لطفاً خطاهای فرم را بررسی و اصلاح کنید.")) #در صورتی که فرم معتبر نباشد
        return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



def update_user(request):
    if request.user.is_authenticated: #ابتدا بررسی می‌کنیم که آیا کاربر وارد شده است یا خیر.
        current_user = User.objects.get(id=request.user.id) # استفاده از request.user.is_authenticated برای بررسی وضعیت ورود
        user_form = UserUpdateForm(request.POST or None, instance = current_user) # استفاده از فرم UserUpdateForm برای بروزرسانی داده‌ها
        if user_form.is_valid(): 
            user_form.save() # ذخیره‌سازی و بروزرسانی اطلاعات
            login(request, current_user) # بروزرسانی اطلاعات کاربر و ورود مجدد به سیستم
            messages.success(request, 'Updated!')
            return redirect('index')
        return render(request, 'update_user.html', {'user_form': user_form})
       
    else:
        messages.error(request, 'login First') # اگر کاربر وارد نشده باشد
        return redirect('index')

def update_password(request):
    if not request.user.is_authenticated:
        messages.error(request, _('لطفاً ابتدا وارد شوید.'))
        return redirect('login')

    current_user = request.user

    if request.method == 'POST':
        form = UpdatePasswordForm(current_user, request.POST)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد.')
            return redirect('update_user')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UpdatePasswordForm(current_user)

    return render(request, 'update_password.html', {'form': form})

def update_info(request):
    if not request.user.is_authenticated:
        messages.error(request, _('لطفاً ابتدا وارد حساب کاربری شوید.'))
        return redirect('login')

    current_user, created = Profile.objects.get_or_create(user=request.user) # اطلاعات کاربر ساخته شده را ذخیره میکنیم تا در مراحل بعدی استفاده کنیم

    if request.method == "POST":
        form = UpdateUserInfo(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, _('اطلاعات با موفقیت بروزرسانی شد.'))
            return redirect('index')
        else:
            messages.error(request, _('Error'))
    else:
        form = UpdateUserInfo(instance=current_user) # نمایش یک فرم خالی برای کاربر و وارد کردن اطلاعات

    return render(request, 'update_info.html', {'form': form})

# هدف این ویو : 
#نمایش یک محصول خاص با آی‌دی مشخص و همچنین امکان ارسال پیام یا نظر کاربر درباره‌ی آن محصول.
def product(request, pk):
    product = get_object_or_404(Product, id=pk) # گرفتن شیء محصول بر اساس شناسه (id)
    messages = ProductMessage.objects.filter(product=product) # گرفتن پیام‌ها (نظرات) مربوط به این محصول

    if request.method == 'POST':
        form = ProductMessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False) # save(commit=False) باعث می‌شه که فعلاً فرم ذخیره نشه
            new_message.product = product
            new_message.user = request.user # نمایش کاربر که نظر ثبت کرده
            new_message.save()
            return redirect('product', pk=product.id) # برای جلوگیری از تکراری پیام بعد از رفرش
    else:
        form = ProductMessageForm() # ایجاد فرم خالی برای نوشتن پیام

    return render(request, 'product.html', { # رندر نهایی به قالب product.html
        'product': product,
        'messages': messages,
        'form': form,
    })

def additionalproduct_detail(request, id):
    product = get_object_or_404(Additionalproduct, id=id) #دریافت ایمن محصول جانبی با id مشخص
    messages = AdditionalProductMessage.objects.filter(product=product)

    if request.method == 'POST':
        form = AdditionalProductMessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.product = product
            new_message.user = request.user 
            new_message.save()
            return redirect('product', pk=product.id)
    else:
        form = AdditionalProductMessageForm()

    return render(request, 'additionalproduct_detail.html', {
        'product': product,
        'messages': messages,
        'form': form,
    })


def additionalproduct(request):
    products = Additionalproduct.objects.all()
    return render(request, 'additionalproduct.html', {'additionalproducts': products})

def contact(request):
    return render(request, 'contact.html')

def category(request, cat): # تعریف تابع و دریافت پارامت
    # cat یک مقدار از url هست مثلا : category/<str:cat> که در url.py تعریف شده
    cat = cat.replace("_", " ") # برای تطبیق با slug موجود در دیتابیس تبدیل خط زیر به فاصله
    try:
        category = Category.objects.get(slug=cat) # سعی می‌کنیم شیء دسته‌بندی مورد نظر را از مدل Category با مقدار slug=cat پیدا کنیم.
        products = Product.objects.filter(category=category) #  فیلتر کردن محصولات بر اساس آن دسته
        return render(request, 'category.html', {
            'products': products,
            'category': category
        })
    except Category.DoesNotExist:
        messages.error(request, f'دسته‌بندی "{cat}" یافت نشد')
        return redirect("index")
