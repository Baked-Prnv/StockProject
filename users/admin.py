from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .forms import MyUserChangeForm, MyUserCreationForm
from .models import *

# Register your models here.

class Useradmin(UserAdmin):
    
    model = User

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser','is_advisor','is_learner', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    list_display = ('username', 'email', 'first_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    search_fields = ('username', 'first_name', 'email')
    ordering = ('email',)


admin.site.register(User, Useradmin)
admin.site.register(Advisor)
admin.site.register(Learner)