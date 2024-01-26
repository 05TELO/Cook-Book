from typing import Any

from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import Product
from .models import Recipe
from .models import RecipeProduct


class HealthcheckView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"message": "healthy"})


class AddProductToRecipe(View):
    """
    View for adding a product to a recipe.
    GET parameters: recipe_id, product_id, weight.
    """

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        try:
            recipe_id = request.GET["recipe_id"]
            product_id = request.GET["product_id"]
            weight = request.GET["weight"]

            recipe_product, created = RecipeProduct.objects.get_or_create(
                recipe_id=recipe_id,
                product_id=product_id,
                defaults={"weight": weight},
            )

            if not created:
                recipe_product.weight = weight
                recipe_product.save()

            return JsonResponse({"status": "Product added to recipe"})

        except KeyError:
            return JsonResponse(
                {"error": "Missing necessary GET parameters."}, status=400
            )
        except (Recipe.DoesNotExist, Product.DoesNotExist):
            raise Http404("Recipe or Product does not exist")


class CookRecipe(View):
    """
    View for cooking a recipe.
    GET parameters: recipe_id.
    """

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        try:
            recipe_id = request.GET["recipe_id"]
            recipe = Recipe.objects.get(id=recipe_id)
            products = recipe.products.all()

            for product in products:
                product.cook_count += 1

            Product.objects.bulk_update(products, ["cook_count"])

            return JsonResponse({"status": f"Recipe {recipe.name} was cooked"})

        except KeyError:
            return JsonResponse(
                {"error": "Missing necessary GET parameters."}, status=400
            )
        except Recipe.DoesNotExist:
            raise Http404("Recipe does not exist")


class ShowRecipesWithoutProduct(View):
    """
    View for showing recipes without a certain product.
    GET parameters: product_id.
    """

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        try:
            product_id = request.GET["product_id"]

            recipes = Recipe.objects.exclude(
                recipeproduct__product_id=product_id,
                recipeproduct__weight__gte=10,
            )

            return render(
                request, "recipes_without_product.html", {"recipes": recipes}
            )

        except KeyError:
            return JsonResponse(
                {"error": "Missing necessary GET parameters."}, status=400
            )
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
