# Create your views here.
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
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

@user_passes_test(admin_only)
def admin_panel(request):
    return redirect('admin:index')

def home(request):    
    context = {
        'welcome_message': _("Hello Welcome!")
    }
    return render(request, 'index.html', context)

def user_orders(request):
    if request.user.is_authenticated:
        delivered_orders = Order.objects.filter(user=request.user, status='Delivered')
        current_orders = Order.objects.filter(user=request.user).exclude(status='Delivered')

        context = {
            'delivered_orders': delivered_orders,
            'current_orders': current_orders,
        }

        return render(request, 'orders.html', context)

    
    else:
        messages.success(request, 'not avilable!')
        return redirect('index')
    
def order_details(request, pk):
    if request.user.is_authenticated:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        context = {
            'order': order,
            'items': items,
        }
        
        return render(request, 'order_details.html', context)
    
    else:
        messages.success(request, 'not avilable!')
        return redirect('index')

def search(request):
    searched = request.POST.get('searched')
    products = Product.objects.filter(
        Q(name__icontains=searched) | Q(description__icontains=searched)
    ) if searched else []
    return render(request, 'search.html', {
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

def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, _("شما قبلاً وارد شده‌اید."))
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', 'index')
            
            if '/admin/' in next_page and not user.is_staff:
                messages.error(request, _("شما دسترسی به پنل مدیریت ندارید"))
                return redirect('index')
                
            return redirect(next_page)
        else:
            messages.error(request, _("نام کاربری یا رمز عبور اشتباه است"))
    
    return render(request, 'login.html')


def signup_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                form.add_error('username', _("این نام کاربری قبلاً ثبت شده است."))
            elif User.objects.filter(email=email).exists():
                form.add_error('email', _("این ایمیل قبلاً ثبت شده است."))
            else:
                user = form.save()
                Profile.objects.get_or_create(user=user)
                login(request, user)
                migrate_session_cart_to_user(request, user)
                messages.success(request, _("اکانت شما ساخته شد."))
                return redirect("index")

        messages.error(request, _("لطفاً خطاهای فرم را بررسی و اصلاح کنید."))
        return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UserUpdateForm(request.POST or None, instance = current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'Updated!')
            return redirect('index')
        return render(request, 'update_user.html', {'user_form': user_form})
       
    else:
        messages.success(request, 'login First')
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

    current_user, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UpdateUserInfo(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, _('اطلاعات با موفقیت بروزرسانی شد.'))
            return redirect('index')
        else:
            messages.error(request, _('اطلاعات با موفقیت بروزرسانی شد.'))
    else:
        form = UpdateUserInfo(instance=current_user)

    return render(request, 'update_info.html', {'form': form})


    
def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    messages = ProductMessage.objects.filter(product=product)

    if request.method == 'POST':
        form = ProductMessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.product = product
            new_message.save()
    else:
        form = ProductMessageForm()

    return render(request, 'product.html', {
        'product': product,
        'messages': messages,
        'form': form,
    })

def additionalproduct_detail(request, id):
    product = get_object_or_404(Additionalproduct, id=id)
    messages = AdditionalProductMessage.objects.filter(product=product)

    if request.method == 'POST':
        form = AdditionalProductMessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.product = product
            new_message.save()
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


def category(request, cat):
    cat = cat.replace("_", " ")
    try:
        category = Category.objects.get(slug=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {
            'products': products,
            'category': category
        })
    except Category.DoesNotExist:
        messages.error(request, f'دسته‌بندی "{cat}" یافت نشد')
        return redirect("index")
