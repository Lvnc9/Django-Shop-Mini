from django.urls import path
from . import views



app_name = "accounts"
urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name='user_register'),
    path("login/", views.UserLoginView.as_view(), name='login'),
    path("logout/", views.UserLogoutView.as_view(), name='logout'),
    path("vairify/", views.UserRegisterVarifyCodeView.as_view(), name="varify_code"),
]