from django.contrib import admin
from .models import Order, OrderItem, Coupon
# Register your models here.



class OrderItemInline(admin.TabularInline):
    ### allow you to edit related models on the same page
    #  as the parent model in the admin interface ###
    
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated', 'paid')
    list_filter = ("paid",)
    inlines = (OrderItemInline,)                           # inline better to be set in another class as we did.

admin.site.register(Coupon)