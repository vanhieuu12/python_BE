from django.contrib import admin
from .models import Product, Category, Order, OrderItem, ProductImage
from django.contrib.auth.models import Group

# --- Category ---
admin.site.register(Category)

# --- OrderItem inline ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity', 'total_price']

    def total_price(self, obj):
        return obj.price * obj.quantity
    total_price.short_description = 'Thành tiền'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # số ô thêm ảnh mặc định
    max_num = 10  # tối đa 10 ảnh



# --- Order admin ---
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'created_at', 'total_amount']

    def total_amount(self, obj):
        return sum(item.price * item.quantity for item in obj.orderitem_set.all())
    total_amount.short_description = 'Thành tiền'


# --- OrderItem admin ---
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity', 'get_total']

    def get_total(self, obj):
        return obj.price * obj.quantity
    get_total.short_description = 'Thành tiền'

# --- Product admin ---
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'user']
    search_fields = ['name']
    list_filter = ['category']
    inlines = [ProductImageInline]

# --- Register models ---
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

# --- Tạo nhóm Admin nếu cần ---
# admin_group, _ = Group.objects.get_or_create(name='Admin')
