from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError

from utils.validators import LETTER_SPACE_DASH_VALIDATOR
from .choices import FoodType, DietType, QuantityUnit


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
    def calories_per_100g(self):
        result = self.protein_per_100g * 4 + self.carbs_per_100g * 4 + self.fats_per_100g * 9
        return result.quantize(Decimal("0.01"))

    def clean(self):
        super().clean()
        if self.default_unit == QuantityUnit.PIECE and self.average_piece_weight <= 0:
            raise ValidationError({"average_piece_weight": "Le poids moyen doit être renseigné."})