from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

class CustomUserAdmin(UserAdmin):
    def has_delete_permission(self, request, obj=None):
        if obj:
            # Check if user has related rides
            if obj.rides_as_rider.exists() or obj.rides_as_driver.exists():
                return False
        return super().has_delete_permission(request, obj)

    def delete_model(self, request, obj):
        # Handle deletion of user with no related rides
        obj.delete()

admin.site.register(CustomUser, CustomUserAdmin)