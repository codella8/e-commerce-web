from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import ProductMessage, AdditionalProductMessage, Profile
from django import forms
from django.utils.translation import gettext_lazy as _

class UpdateUserInfo(forms.ModelForm):
    phone = forms.CharField(
        label="", 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('تلفن')})
    )
    address1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('1 آدرس')}),
        required=False
    )
    address2 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('2 آدرس')}),
        required=False
    )
    city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('شهر')}),
        required=False
    )
    country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('کشور')}),
        required=False
    )
    
    
    class Meta:
        model = Profile
        fields = ['phone', 'address1', 'address2', 'city', 'country']

class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('رمز جدید را وارد کنید')
            }
        )
    )

    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('رمز جدید را دوباره وارد کنید')
            }
        )
    )

class UserUpdateForm(UserChangeForm):
    password = None
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('اسم')}),
        required=False
    )


    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('نام خانوادگی')}),
        required=False
    )

    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('ایمیل')}),
        required=False
    )

    username = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('نام کاربری')}),
        required=False
    )
     

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('نام ')})
    )


    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('نام خانوادگی')})
    )

    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('ایمیل')})
    )

    username = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('نام کاربری')})
    )

    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'name': 'password1',
                'type': 'password1',
                'placeholder': _('رمز خودرا وارد کنید')
            }
        )
    )

    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'name': 'password2',
                'type': 'password2',
                'placeholder': _('دوباره رمز خودرا وارد کنید')
            }
        )
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        
class ProductMessageForm(forms.ModelForm):
    class Meta:
        model = ProductMessage
        fields = ['name', 'email', 'message']
        
class AdditionalProductMessageForm(forms.ModelForm):
    class Meta:
        model = AdditionalProductMessage
        fields = ['name', 'email', 'message']