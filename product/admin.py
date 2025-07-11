from django.contrib import admin
from .models import Product, Category, Order, OrderItem
from django.contrib.auth.models import Group

admin.site.register(Product)
admin.site.register(Category)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity', 'total_price']

    def total_price(self, obj):
        return obj.price * obj.quantity
    total_price.short_description = 'Thành tiền'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'created_at', 'get_total']
    list_filter = ['created_at']
    search_fields = ['name', 'phone', 'address']
    inlines = [OrderItemInline]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity', 'get_total']

    def get_total(self, obj):
        return obj.price * obj.quantity
    get_total.short_description = 'Thành tiền'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

# (Tuỳ chọn) Tạo nhóm người dùng
admin_group, _ = Group.objects.get_or_create(name='Admin')
