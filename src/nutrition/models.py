from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from utils.validators import LETTER_SPACE_DASH_VALIDATOR
from .choices import FoodType, DietType, QuantityUnit

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100, validators=[LETTER_SPACE_DASH_VALIDATOR], verbose_name="Nom")
    food_type = models.CharField(max_length=10, choices=FoodType, verbose_name="Type d'aliment")
    diet_type = models.CharField(max_length=10, choices=DietType, verbose_name="Type de régime")
    default_unit = models.CharField(max_length=10, choices=QuantityUnit, verbose_name="Unité par défaut")

    protein_per_100g = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Protéines pour 100g",
                                           default=0.00)
    carbs_per_100g = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Glucides pour 100g",
                                         default=0.00)
    fats_per_100g = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Lipides pour 100g", default=0.00)

    average_piece_weight = models.PositiveIntegerField(verbose_name="Poids moyen par pièce (g)", default=0)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        verbose_name = "Ingrédient"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name", "food_type"], name="unique_ingredient_name")
        ]

    def __str__(self):
        return f"{self.name}"

    @property
    # dynamic calcul, not in database
    def calories_per_100g(self):
        result = self.protein_per_100g * 4 + self.carbs_per_100g * 4 + self.fats_per_100g * 9
        return result.quantize(Decimal("0.01"))

    # clean is not automatically call by save method: only with admin form, model form, not in memory test instance
    def clean(self):
        super().clean()
        if self.default_unit == QuantityUnit.PIECE and self.average_piece_weight <= 0:
            raise ValidationError({"average_piece_weight": "Le poids moyen doit être renseigné."})


class Plate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur", related_name="plates")
    name = models.CharField(max_length=100, verbose_name="Nom du plat")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        verbose_name = "Plat"

    def __str__(self):
        return f"{self.name} - {self.user}"

    def nutritional_profile(self):
        # get all ingredients of current plate
        # plate_ingredients = self.ingredients.all() # NOT SQL OPTIMIZE
        plate_ingredients = self.ingredients.select_related("ingredient").all() # SQL OPTIMIZE (one time)
        total_protein = 0
        total_carbs = 0
        total_fats = 0
        total_calories = 0

        for plate_ingredient in plate_ingredients:
            nutritional_values = plate_ingredient.get_nutritional_values()
            total_protein += nutritional_values["protein"] # /!\ use Decimal ?
            total_carbs += nutritional_values["carbs"]
            total_fats += nutritional_values["fats"]
            total_calories += nutritional_values["calories"]

        return {
            "total_protein": total_protein,
            "total_carbs": total_carbs,
            "total_fats": total_fats,
            "total_calories": total_calories,
        }


class PlateIngredient(models.Model):
    plate = models.ForeignKey(Plate, on_delete=models.CASCADE, related_name="ingredients", verbose_name="Plat")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ingrédient")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")

    class Meta:
        verbose_name = "Ingrédient du plat"
        verbose_name_plural = "Ingrédients du plat"
        unique_together = ("plate", "ingredient")

    def __str__(self):
        return f"{self.quantity} {self.ingredient.default_unit} de {self.ingredient.name} dans {self.plate.name}"

    def get_nutritional_values(self):
        quantity_in_grams = self._convert_to_grams()

        protein_per_gram = self.ingredient.protein_per_100g / 100
        carbs_per_gram = self.ingredient.carbs_per_100g / 100
        fats_per_gram = self.ingredient.fats_per_100g / 100
        calories_per_gram = self.ingredient.calories_per_100g / 100

        return {
            "protein": protein_per_gram * quantity_in_grams,
            "carbs": carbs_per_gram * quantity_in_grams,
            "fats": fats_per_gram * quantity_in_grams,
            "calories": calories_per_gram * quantity_in_grams,
        }

    def _convert_to_grams(self):
        if self.ingredient.default_unit == QuantityUnit.GRAM:
            return self.quantity
        else:  # sinon pièce
            return self.quantity * self.ingredient.average_piece_weight

    def display_unit(self):
        if self.ingredient.default_unit == QuantityUnit.GRAM:
            return "g"
        else:
            return "p"
