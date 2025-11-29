from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Додатково', {'fields': ('role', 'avatar', 'phone', 'bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Додатково', {'fields': ('role', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)