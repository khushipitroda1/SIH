from re import A
from django.contrib import admin

from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id','username','is_staff','is_active',)
    list_filter = ('email','is_staff','is_active',)
    fieldsets = (
        (None, {'fields':('email','password','user_type')}),
        ('Permissions',{'fields': ('is_staff','is_active')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('username','email','user_type','password1','password2','is_staff','is_active')
        }),
    )


# admin.site.register(UserType)

# admin.site.unregister(User)
admin.site.register(CustomUser,CustomUserAdmin)