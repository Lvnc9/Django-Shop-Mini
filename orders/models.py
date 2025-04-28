from django.db import models
# the models gets used as the user model set to the setting which is the refrence
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from home.models import Product


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name="orders")
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # blank=True : let the form be empty at the admin/Order
    # null=True : let it have a null value in database if it hasn't any value.
    discount = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        # -updated: the newst updated
        ordering = ("paid", "-updated")
    
    def __str__(self):
        return f"{self.user} - {self.id}"

    def get_total(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount = total * (self.discount / 100)
            total = total - discount

        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code