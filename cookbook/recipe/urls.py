from django.urls import path

from . import views

app_name = "recipe"

urlpatterns = [
    path("", views.index, name="recipes"),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_detail.html"),
    path(
        "change_product_in_recipe/<int:recipe_id>/",
        views.add_product_to_recipe,
        name="add_product_to_recipe",
    ),
    path("cook_recipe/<int:recipe_id>/", views.cook_recipe, name="cook_recipe"),
    path(
        "recipes_without_product/<int:product_id>/",
        views.show_recipes_without_product,
        name="recipes_without_product",
    ),
]
