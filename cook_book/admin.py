from django.contrib import admin

from .models import Product
from .models import Recipe
from .models import RecipeProduct


class RecipeProductInline(admin.TabularInline):
    model = RecipeProduct
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "cook_count"]
    search_fields = ["name"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [RecipeProductInline]
    search_fields = ["name"]
