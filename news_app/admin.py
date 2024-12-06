from django.contrib import admin
from .models import SearchQuery, Article
from django.contrib.auth.models import User

admin.site.register(SearchQuery)
admin.site.register(Article)

admin.site.unregister(User)



from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')  # Optional: for easy search by username/email
    actions = ['block_users', 'unblock_users']

    def block_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected users have been blocked.")

    def unblock_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected users have been unblocked.")

    block_users.short_description = "Block selected users"
    unblock_users.short_description = "Unblock selected users"




# @admin.register(User)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_active')
#     list_filter = ('is_active', 'is_staff', 'is_superuser')
#     actions = ['block_users', 'unblock_users']

#     def block_users(self, request, queryset):
#         queryset.update(is_active=False)
#         self.message_user(request, "Selected users have been blocked.")

#     def unblock_users(self, request, queryset):
#         queryset.update(is_active=True)
#         self.message_user(request, "Selected users have been unblocked.")

#     block_users.short_description = "Block selected users"
#     unblock_users.short_description = "Unblock selected users"




