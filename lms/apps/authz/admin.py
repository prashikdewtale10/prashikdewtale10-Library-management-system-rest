from django.contrib import admin
from django.contrib.auth import get_user_model


# --- Custom User model ---
User = get_user_model()


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    # ordering = ["username"]
    search_fields = ["username"]
    sortable_by = ["role"]
    list_display = ["id", "username", "first_name", "last_name", "role"]


admin.site.register(User, UserAdmin)
