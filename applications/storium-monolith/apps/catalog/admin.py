from django.contrib import admin

from apps.catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "is_active", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["is_active", "parent"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "is_active", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["is_active", "category"]
    search_fields = ["name", "description"]
    list_editable = ["price", "stock", "is_active"]
