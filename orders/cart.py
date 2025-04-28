from home.models import Product

CART_SESSION_ID = 'cart'

class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)            # Session itself is a dictionary.
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}             # submitting a new key
        
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product  # Product model in __str__ set to return product.name!

        for item in cart.values():
            if 'price' in item and 'quantity' in item:  # Ensure 'price' and 'quantity' exist
                try:
                    item['total_price'] = int(item['price']) * int(item['quantity'])
                    yield item
                except (ValueError, TypeError):
                    # Handle invalid data gracefully
                    continue  
    def __len__(self):
        try:
            return sum(int(item.get('quantity', 0)) for item in self.cart.values())
        except (ValueError, TypeError):
            return 0  # Return 0 if there is invalid data

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity":0, "price":str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def save(self):
        self.session.modified = True                        # to save sessions need to set modified to True


    def get_total_price(self):
        try:
            total = sum(int(item.get("total_price", 0)) for item in self.cart.values())
            if total == 0:
                return "Your basket is empty! 😉"
            return total
        except (ValueError, TypeError):
            return "Your basket contains invalid data."

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
