from django.db import models


class FoodType(models.TextChoices):
    PROTEIN = "PROT", "Protein"
    VEGETABLE = "VEG", "Vegetable"
    FRUIT = "FRUIT", "Fruit"


class DietType(models.TextChoices):
    OMNIVORE = "OMNI", "Omnivore"
    VEGETARIAN = "VEGE", "Vegetarien"
    VEGAN = "VEGAN", "VEGAN"


class QuantityUnit(models.TextChoices):
    GRAM = "G", "Gram"
    PIECE = "P", "Piece"
