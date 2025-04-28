from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import UserRegisterationForm, VarifyCodeForm, UserLoginForm
from .models import OtpCode, User
from utils import send_otp_code
import random
# Create your views here.

class UserRegisterView(View):
    form_class = UserRegisterationForm
    template_name = "accounts/register.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                "phone_number" : form.cleaned_data['phone_number'],
                "email" : form.cleaned_data['email'],
                "full_name" : form.cleaned_data['full_name'],
                "password" : form.cleaned_data['password'],
            }
            print(f"This is email: {form.cleaned_data['email']}")
            
            messages.success(request, "We've sent you a code", "success")
            return redirect("accounts:varify_code")

        messages.error(request, "Wrong", "warning")
        return render(request, self.template_name, {"form":form})
    

class UserRegisterVarifyCodeView(View):
    form_class = VarifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/varify.html", {"form":form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])

        print(code_instance)
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(
                    email=user_session['email'],
                    phone_number=user_session['phone_number'],
                    full_name=user_session['full_name'],
                    password=user_session['password'], 
                )
                
                code_instance.delete()
                messages.success(request, "user registered", "success")
                return redirect("home:home")
            else:
                messages.error(request, "This code is wrong", "danger")
                return redirect("accounts:varify_code")

class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, "Successfully Logedout", "success")
        return redirect("home:home")

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "accounts/login.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "you logged in successfully", 'success')
                return redirect("home:home")
            messages.error(request, "phone or password is wrong", "warning")
        return render(request, self.template_name, {'form':form})
