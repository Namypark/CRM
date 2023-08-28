from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    model = Account
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superadmin",
    )
    list_filter = ("email", "first_name", "last_name", "is_staff", "is_active")
    readonly_fields = (
        "last_login",
        "date_joined",
    )
    ordering = ("date_joined",)
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
