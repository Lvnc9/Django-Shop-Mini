from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category
from utils import IsAdminUserMixin
from orders.forms import CartAddForm
from . import tasks

# Create your views here.

class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)

        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category)
        return render(request, 'home/home.html', {'products':products, "categories":categories})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        forms = CartAddForm()

        return render(request, 'home/detail.html', {"product":product, "form":forms})
    

class BucketHome(IsAdminUserMixin, View):
    template_name = "home/bucket.html"

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {"objects":objects})


class DeleteObject(IsAdminUserMixin, View):
    
    def dispatch(self, request, *args, **kwargs):

        return super().dispatch(request, *args, **kwargs)
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, "your object will be deleted soon.")        
        return redirect('home:bucket')
    
class DownloadObject(IsAdminUserMixin, View):

    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, "your object is started downloading")
        return redirect("home:bucket")
