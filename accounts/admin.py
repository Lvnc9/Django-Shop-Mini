from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserChangeForm, UserCreationForm
from .models import User, OtpCode
# Register your models here.



    
@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')

    
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "phone_number", "is_admin")
    list_filter = ("is_admin",)
    readonly_fields = ("last_login",)

    fieldsets = (
        (None, {"fields":('email', 'phone_number', 'full_name', 'password')}),
        ("Permissions", {'fields':('is_active','is_admin', 'is_superuser', 'last_login', "groups", "user_permissions")}),
        )

    add_fieldsets = (
        (None, {'fields':('phone_number', 'email', 'full_name', 'password1', 'password2', 'is_superuser')}),
    )
    
    search_fields = ('email', 'full_name')
    ordering = ("full_name",)
    filter_horizontal = ('groups', 'user_permissions')


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_super = request.user.is_superuser
        if not is_super and 'is_superuser' in form.base_fields:
            form.base_fields['is_superuser'].disabled = True
        return form

#admin.site.unregister(Group)
admin.site.register(User, UserAdmin)