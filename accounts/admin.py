from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("NOK fields", {"fields": ("role", "display_name", "referral_code", "referred_by", "xp", "streak_days")}),
    )
    list_display = ("username", "display_name", "role", "email", "referral_code", "referred_by", "xp", "streak_days")
