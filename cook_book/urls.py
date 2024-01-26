from django.urls import path

from .views import AddProductToRecipe
from .views import CookRecipe
from .views import HealthcheckView
from .views import ShowRecipesWithoutProduct

urlpatterns = [
    path("healthcheck/", HealthcheckView.as_view(), name="healthcheck"),
    path(
        "add_product_to_recipe/",
        AddProductToRecipe.as_view(),
        name="add_product_to_recipe",
    ),
    path("cook_recipe/", CookRecipe.as_view(), name="cook_recipe"),
    path(
        "show_recipes_without_product/",
        ShowRecipesWithoutProduct.as_view(),
        name="show_recipes_without_product",
    ),
]
