from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile, User

login_required

# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The form fields to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff',)
    readonly_fields = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'is_superuser',
                'is_staff')
        }
         ),
    )
    search_fields = ('username', 'email')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(UserProfile)
admin.site.register(User, UserAdmin)
