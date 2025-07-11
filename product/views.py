from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Count
import csv
from django.http import HttpResponse
from django.contrib.auth.models import Group
from openpyxl import Workbook
from .models import Category
from django.shortcuts import redirect, get_object_or_404
from .models import Product
from .cart import Cart
from django.shortcuts import render
from .forms import OrderForm
from .models import Order, OrderItem
from django.shortcuts import render, redirect
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Order


@login_required
def product_list(request):
    products = Product.objects.all()  # 👈 Hiển thị toàn bộ sản phẩm cho cả user và admin

    query = request.GET.get('q')
    category_filter = request.GET.get('category')

    if query:
        products = products.filter(name__icontains=query)
    if category_filter:
        products = products.filter(category__name__icontains=category_filter)

    products = products.order_by('-id')
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product/list.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'query': query,
        'category_filter': category_filter,
        'categories': Category.objects.all(),
    })


@login_required
def product_stats(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Chỉ admin mới xem được thống kê.")
    
    stats = User.objects.annotate(product_count=Count('product')).order_by('-product_count')
    return render(request, 'product/stats.html', {'stats': stats})



def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return redirect('product_list')
    return render(request, 'product/form.html', {'form': form})




def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.user and not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền sửa sản phẩm này.")
    
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'product/form.html', {'form': form})



def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.user and not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền xoá sản phẩm này.")
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product/delete.html', {'product': product})

from django.contrib.auth.models import Group

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()

        # ✅ Gán user vào nhóm 'Seller'
        seller_group, _ = Group.objects.get_or_create(name='Seller')
        user.groups.add(seller_group)

        login(request, user)
        return redirect('product_list')
    return render(request, 'product/register.html', {'form': form})


@login_required
def export_products_csv(request):
    if not request.user.is_superuser:
        return HttpResponse("Chỉ admin được phép xuất dữ liệu.", status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['Tên sản phẩm', 'Giá', 'Người tạo', 'Mô tả'])

    for product in Product.objects.all():
        writer.writerow([product.name, product.price, product.user.username, product.description])

    return response
@login_required
def export_products_excel(request):
    if not request.user.is_superuser:
        return HttpResponse("Chỉ admin được phép xuất dữ liệu.", status=403)

    wb = Workbook()
    ws = wb.active
    ws.title = "Products"

    ws.append(['Tên sản phẩm', 'Giá', 'Người tạo', 'Mô tả'])
    for p in Product.objects.all():
        ws.append([p.name, float(p.price), p.user.username, p.description])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    wb.save(response)
    return response

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/detail.html', {'product': product})


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.add(product)
    return redirect('view_cart')

from django.shortcuts import get_object_or_404, redirect
from .cart import Cart
from .models import Product

def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)

    print("🗑 Đang cố xoá:", pk)
    print("📦 Cart trước xoá:", request.session.get('cart'))

    cart.remove(product)

    print("✅ Đã xoá:", pk)
    print("📦 Cart sau xoá:", request.session.get('cart'))

    return redirect('view_cart')




def update_cart(request):
    cart = Cart(request)

    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("quantity_"):
                try:
                    product_id = key.split("_")[1]
                    quantity = int(value)

                    product = Product.objects.get(pk=product_id)

                    cart.update(product, quantity)  # ✅ Gọi phương thức update
                except (Product.DoesNotExist, ValueError):
                    continue

    return redirect('view_cart')


def view_cart(request):
    cart = Cart(request)
    return render(request, 'product/cart.html', {'cart': cart})

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart = Cart(request)

    if not any(cart):
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                note=form.cleaned_data['note']
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()

            return render(request, 'product/checkout_success.html', {
                'order': order,
                'items': order.items.all()
            })
    else:
        form = OrderForm()

    return render(request, 'product/checkout.html', {'form': form, 'cart': cart})

def clear_cart(request):
    request.session['cart'] = {}
    return HttpResponse("🧹 Cart cleared")


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'product/order_history.html', {'orders': orders})