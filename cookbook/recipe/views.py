from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page

from .models import Products, Recipe, RecipeProducts


def paginator_get_page(queryset, request):
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


@cache_page(20)
def index(request):
    return render(
        request,
        "index.html",
        {"page_obj": paginator_get_page(Recipe.objects.all(), request)},
    )


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_products = RecipeProducts.objects.filter(recipe=recipe)
    context = {"recipe": recipe, "recipe_products": recipe_products}
    return render(request, "recipe_detail.html", context)


def add_product_to_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        weight = request.POST.get("weight")
        product = get_object_or_404(Products, name=product_name)
        recipe_product, created = RecipeProducts.objects.get_or_create(
            recipe=recipe, products=product, defaults={"weight": weight}
        )
        if not created:
            recipe_product.weight = weight
            recipe_product.save()
        return HttpResponse("Продукты добавлены в рецепт.")
    else:
        context = {
            "recipe": recipe,
        }
        return render(request, "change_product_in_recipe.html", context)


def cook_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_products = RecipeProducts.objects.select_related("products").filter(
        recipe=recipe
    )
    for recipe_product in recipe_products:
        product = recipe_product.products
        product.cooking_amount = F("cooking_amount") + 1
        product.save(update_fields=["cooking_amount"])
    context = {"recipe": recipe, "recipe_products": recipe_products}
    return render(request, "cook_recipe.html", context)


def show_recipes_without_product(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    recipes_less_than_10g = Recipe.objects.filter(
        recipeproducts__products=product, recipeproducts__weight__lt=10
    )
    context = {"recipes": recipes_less_than_10g, "product": product}
    return render(request, "recipes_without_product.html", context)
