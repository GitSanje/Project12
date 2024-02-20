from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .forms import UserRegistrationForm
from accounts.models import User,Profile,FriendRequest


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','full_name']

class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user' ,'bio']

admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(FriendRequest)
# class CustomUserAdmin(UserAdmin):
#     add_form = UserRegistrationForm
#     add_fieldsets = (
#         (None, {
#             'fields': ('username', 'full_name', 'email', 'password1', 'password2'),
#         }),
#     )
#     list_display = ['username', 'display_full_name', 'email', 'is_staff']
#
#     def display_full_name(self, obj):
#         return obj.full_name
#     display_full_name.short_description = 'Full Name'
# #
# admin.site.unregister(get_user_model())
# admin.site.register(get_user_model(), CustomUserAdmin)


