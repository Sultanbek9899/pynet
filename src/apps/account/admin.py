from django.contrib import admin

from src.apps.account.models import User

from src.apps.account.forms import UserRegisterForm

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserRegisterForm
    list_display = ["username", "email"]
    filter_horizontal = ["followers"]

# admin.site.register(Follow)