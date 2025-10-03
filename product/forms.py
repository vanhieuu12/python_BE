from django import forms
from .models import Product, Order
from .models import Review   

from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'image']  # bỏ stock, thêm image
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
        }
class OrderForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':2}))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':2}))

class CheckoutForm(forms.Form):
    name = forms.CharField(label="Họ tên", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Số điện thoại", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="Địa chỉ", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    note = forms.CharField(label="Ghi chú", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), required=False)


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']  # <- dùng tên field đúng
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Viết bình luận...'
            }),
            'rating': forms.HiddenInput(),
        }