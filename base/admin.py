from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser 

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informasi Tambahan', {'fields': ('nik',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informasi Tambahan', {'fields': ('nik',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'nik')
    
admin.site.register(CustomUser, CustomUserAdmin)