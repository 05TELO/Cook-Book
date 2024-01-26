from django.db import models


class Product(models.Model):
    name = models.CharField()
    cook_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    name = models.CharField()
    products = models.ManyToManyField(Product, through="RecipeProduct")

    def __str__(self) -> str:
        return self.name


class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()
