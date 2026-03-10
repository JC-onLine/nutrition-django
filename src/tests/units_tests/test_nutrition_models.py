import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from nutrition.models import Ingredient, Plate, PlateIngredient
from nutrition.choices import QuantityUnit, FoodType, DietType

User = get_user_model()


@pytest.mark.django_db
# test @property of Ingredient model
def test_calories_per_100g(ingredient_gram):
    expected_calories = (Decimal("27.00") * 4) + (Decimal("0.00") * 4) + (Decimal("3.60") * 9)
    assert ingredient_gram.calories_per_100g == expected_calories


@pytest.mark.django_db
# test clean method of Ingredient model, without average weight
def test_clean_validation_piece_without_weight():
    """
    Given with unit piece but without weight
    When validation
    Then raise ValidationError
    """
    ingredient = Ingredient( # instance = database
        name="test",
        food_type=FoodType.FRUIT,
        diet_type=DietType.VEGAN,
        default_unit=QuantityUnit.PIECE,
        average_piece_weight=0 # weight = zero
    )
    # will raise ValidationError
    with pytest.raises(ValidationError):
        ingredient.clean()


@pytest.mark.django_db
# create new ingredient whit same name and same food_type of ingredient_gram() fixture
def test_unique_together_constraint(ingredient_gram):
    """
    Given ingredient_gram() fixture data
    When creation
    Then raise IntegrityError
    Because
        constraints = [
                    models.UniqueConstraint(fields=["name", "food_type"], name="unique_ingredient_name")
                ]
    """
    with pytest.raises(IntegrityError):
        Ingredient.objects.create(
            name=ingredient_gram.name,
            food_type=ingredient_gram.food_type,
            diet_type=DietType.OMNIVORE,
            default_unit=QuantityUnit.GRAM,
            protein_per_100g=Decimal("10.00"),
            carbs_per_100g=Decimal("5.00"),
            fats_per_100g=Decimal("2.00")
        )


@pytest.mark.django_db
# create new PlateIngredient whit same plate and ingredient of add_plate_ingredient_num1() fixture
def test_unique_together_plate_ingredient_constraint(add_plate_ingredient_num1):
    """
    Given add_plate_ingredient_num1() fixture data
    When creation
    Then raise IntegrityError
    Because
        unique_together = ("plate", "ingredient")
    """
    with pytest.raises(IntegrityError):
        PlateIngredient.objects.create(
            plate=add_plate_ingredient_num1.plate,
            ingredient=add_plate_ingredient_num1.ingredient,
            quantity=add_plate_ingredient_num1.quantity,
        )
