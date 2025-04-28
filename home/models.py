from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.

class Category(models.Model):
    sub_category = models.ForeignKey("self", on_delete=models.CASCADE, related_name="scategory", null=True, blank=True)
    is_sub = models.BooleanField(default=False)

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = "category"               # how the model get pronounce when you enter the model.
        verbose_name_plural = "Categories"      # used for plural in direct models part of admin

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("home:category_filter", args=[self.slug])

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    # use upload_to=https://t.me/PersianDevHub if you are hosting in local
    image = models.ImageField()
    description = RichTextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("home:product_detail", args=[self.slug,])