from django.contrib import admin

from .models import Products, Recipe, RecipeProducts


class RecipeProductsInline(admin.TabularInline):
    model = RecipeProducts
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeProductsInline,)
    list_display = ("pk", "name", "_products")
    list_editable = ("name",)
    search_fields = ("name", "_products")
    list_filter = ("name", "products")
    empty_value_display = "-пусто-"

    def _products(self, row):
        return ", ".join([x.name for x in row.products.all()])

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        form.save_m2m()
        if not form.cleaned_data.get("products"):
            super().save_model(request, obj, form, change)

    def cook_recipe(self, request, queryset):
        for recipe in queryset:
            recipe_products = RecipeProducts.objects.filter(recipe=recipe)
            for recipe_product in recipe_products:
                product = recipe_product.products
                product.cooking_amount += 1
                product.save()
        self.message_user(request, "Количество приготовлений изменено.")

    cook_recipe.short_description = "Изменить количество приготовлений"
    actions = [cook_recipe]


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "measurement_units", "cooking_amount")
    list_filter = ("name",)
    search_fields = ("name",)
