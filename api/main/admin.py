from django.contrib import admin
from django.contrib.auth import get_user_model
from ordered_model.admin import OrderedModelAdmin

from .models import Product, Category

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {"fields": ("id", "password")}),
    #     ("Important dates", {"fields": ("last_login",)}),
    # )
    list_display = ["id", "username", "fullname", "is_admin"]
    list_display_links = ['id', 'fullname']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(OrderedModelAdmin):
    list_display = ["name_uz", "category", "move_up_down_links", "name_ru", "name_en", "order"]
    readonly_fields = ("photo_uri", "photo_updated")
    list_select_related = ["category"]
    ordering = ["order", "category"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...
