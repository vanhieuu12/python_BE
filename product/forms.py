from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class OrderForm(forms.Form):
    name = forms.CharField(label="Họ tên", max_length=100)
    phone = forms.CharField(label="Số điện thoại", max_length=20)
    address = forms.CharField(label="Địa chỉ", widget=forms.Textarea)
    note = forms.CharField(label="Ghi chú", widget=forms.Textarea, required=False)



class CheckoutForm(forms.Form):
    full_name = forms.CharField(label="👤 Họ và tên người nhận", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nhập họ và tên...'
    }))
    phone = forms.CharField(label="📞 Số điện thoại", max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nhập số điện thoại...'
    }))
    address = forms.CharField(label="📍 Địa chỉ", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 1,
        'placeholder': 'Nhập địa chỉ giao hàng...'
    }))
    note = forms.CharField(label="📝 Ghi chú", required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 1,
        'placeholder': 'Ghi chú thêm (nếu có)...'
    }))

