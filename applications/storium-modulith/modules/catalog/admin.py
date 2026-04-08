from django.contrib import admin

from core.services.catalog_service import invalidate_category_nav_cache
from modules.catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "is_active", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["is_active", "parent"]
    search_fields = ["name"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        invalidate_category_nav_cache()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        invalidate_category_nav_cache()

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        invalidate_category_nav_cache()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "is_active", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["is_active", "category"]
    search_fields = ["name", "description"]
    list_editable = ["price", "stock", "is_active"]
