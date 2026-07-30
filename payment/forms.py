from django import forms
from . models import PaymentAddress
from django.utils.translation import gettext_lazy as _

class PaymentAddressForm(forms.ModelForm):
    shipping_full_name = forms.CharField(
        label= '',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full_name'}),
        required=True,
    )
    
    shipping_email = forms.CharField(
        label= '',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True,
    )
    
    shipping_phone = forms.CharField(
        label= '',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        required=True,
    )
    
    
    shipping_address1 = forms.CharField(
        label= '',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address1'}),
        required=True,
    )
    
    shipping_address2 = forms.CharField(
        label= '',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address2'}),
        required=False
    )
    
    shipping_country = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        required=False
    )
    shipping_city = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        required=True
    )
    
    shipping_state = forms.CharField(
        label= '',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
        required=False
    )
    
    
    shipping_zipcode = forms.CharField(
        label= '',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
        required=False
    )
    
    class Meta:
        model = PaymentAddress
        fields = [
            'shipping_full_name',
            'shipping_email',
            'shipping_address1',
            'shipping_address2',
            'shipping_phone',
            'shipping_city',
            'shipping_state',
            'shipping_zipcode',
            'shipping_country',
        ]
        
        exclude = ['user', ]
    
    
    
    