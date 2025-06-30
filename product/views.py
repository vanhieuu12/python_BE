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






@login_required
def product_list(request):
    if request.user.is_superuser:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    products = products.order_by('-id')  # ← thêm dòng này

    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product/list.html', {
        'products': page_obj,
        'page_obj': page_obj,
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

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
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