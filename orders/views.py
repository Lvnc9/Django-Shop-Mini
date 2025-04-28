from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import View
from django.contrib import messages
from home.models import Product
from datetime import datetime
from .cart import Cart
from .forms import CartAddForm, CouponForm
from .models import Order, OrderItem, Coupon
# Create your views here.


class CartView(View):

    def get(self, request):
        cart = Cart(request)
        return render(request, "orders/cart.html", {"cart":cart})
    

class CartAddView(PermissionRequiredMixin, View):
    #def dispatch(self, request, *args, **kwargs):                   # you can do this or...
    #    if not request.user.has_perm("orders.add_order"):
    #        raise PermissionDenied()
    #    return super().dispatch(request, *args, **kwargs)

    permission_required = "orders.add_order"

    def post(self, request, product_id):     
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect("orders:cart")
    

class CartRemoveView(View):

    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect("orders:cart")


class OrderDetailView(View):
    form_class = CouponForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
    
        return render(request, "orders/order.html", {'order':order, "coupon":self.form_class})



class OrderCreateView(View):

    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user,)

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
            )
        cart.clear()
        return redirect("orders:order_detail", order.id)


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponForm

    def post(self, request, order_id):
        now = datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                coupon = Coupon.objects.get(
                    code__exact=cd['code'],
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True
                    )
            except Coupon.DoesNotExist:
                messages.error(request, "Your Coupon either expired or doesn't exists!", "danger")
                return redirect("orders:order_detail", order_id)
        
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect("orders:order_detail", order_id)
