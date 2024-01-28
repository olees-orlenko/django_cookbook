from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Products(models.Model):
    name = models.CharField(
        "Название продукта", max_length=200, help_text="Название продукта"
    )
    measurement_units = models.CharField(
        "Единицы измерения", max_length=200, help_text="Единицы измерения", default="г"
    )
    cooking_amount = models.PositiveSmallIntegerField(
        "Количество приготовлений", help_text="Количество приготовлений", default=0
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_units"], name="name_measurement_units"
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        "Название рецепта", max_length=200, help_text="Название", unique=True
    )
    products = models.ManyToManyField(
        Products,
        related_name="recipe_products",
        through="RecipeProducts",
        through_fields=("recipe", "products"),
        verbose_name="Продукты",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-name",)

    def __str__(self):
        return self.name


class RecipeProducts(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipeproducts",
        verbose_name="Рецепт",
    )
    products = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name="recipeproducts",
        verbose_name="Продукты",
    )
    weight = models.PositiveSmallIntegerField(
        "Вес продукта", validators=[MaxValueValidator(5000), MinValueValidator(1)]
    )
    measurement_units = models.CharField(
        "Единицы измерения", max_length=200, help_text="Единицы измерения", default="г"
    )

    class Meta:
        verbose_name = "Продукты рецепта"
        verbose_name_plural = "Продукты рецептов"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "products"], name="recipe_products"
            )
        ]

    def __str__(self):
        return f"{self.recipe} {self.products}"
