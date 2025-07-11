from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart or not isinstance(cart, dict):
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)

        # Nếu chưa có hoặc đang lỗi kiểu (int) thì tạo lại
        if product_id not in self.cart or not isinstance(self.cart[product_id], dict):
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        self.cart[product_id]['quantity'] += quantity
        self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.remove(product)
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save() 

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            product_id = str(product.id)
            item = self.cart.get(product_id)

            if not isinstance(item, dict):
                continue

            try:
                cart_item = item.copy()
                cart_item['product'] = product
                cart_item['price'] = Decimal(cart_item['price'])
                cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
                yield cart_item
            except (KeyError, ValueError, TypeError):
                continue

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
            if isinstance(item, dict) and 'price' in item
        )
