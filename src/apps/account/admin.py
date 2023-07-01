from django.contrib import admin

from src.apps.account.models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]
    filter_horizontal = ["followers"]

# admin.site.register(Follow)