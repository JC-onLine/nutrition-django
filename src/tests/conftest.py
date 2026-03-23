import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
# application models
from nutrition.models import Ingredient, Plate, PlateIngredient
from nutrition.choices import QuantityUnit, FoodType, DietType
# instance de la classe User
User = get_user_model()


@pytest.fixture
def user1(): # user1 est une fixture qui peut s'appuyer sur d'autres fixtures'
    return  User.objects.create_user(username="user1",
                                     email="test@example.com",
                                     password="motdepasse123456")


@pytest.fixture
def user2():
    return User.objects.create_user(username="user2",
                                    email="test2@example.com",
                                    password="motdepasse123456")


@pytest.fixture
def plates_user1(user1):
    plate1 = Plate.objects.create(user=user1, name="Plat 1 user1 poulet")
    plate2 = Plate.objects.create(user=user1, name="Plat 2 user1")
    return [plate1, plate2]


@pytest.fixture
def plates_user2(user2):
    plate1 = Plate.objects.create(user=user2, name="Plat 1 user2")
    plate2 = Plate.objects.create(user=user2, name="Plat 2 user2")
    return [plate1, plate2]


@pytest.fixture
def ingredient_gram():
    return Ingredient.objects.create(
        name="Poulet",
        food_type=FoodType.PROTEIN,
        diet_type=DietType.OMNIVORE,
        default_unit=QuantityUnit.GRAM,
        protein_per_100g=Decimal("27.00"),
        carbs_per_100g=Decimal("0.00"),
        fats_per_100g=Decimal("3.60")
    )


@pytest.fixture
def ingredient_piece():
    return Ingredient.objects.create(
        name="Oeuf",
        food_type=FoodType.PROTEIN,
        diet_type=DietType.OMNIVORE,
        default_unit=QuantityUnit.PIECE,
        protein_per_100g=Decimal("13.00"),
        carbs_per_100g=Decimal("1.10"),
        fats_per_100g=Decimal("11.00"),
        average_piece_weight=50
    )

@pytest.fixture
def add_plate_ingredient_num1(user1):
    return PlateIngredient.objects.create(
        plate=Plate.objects.create(
            user = user1,
            name="Poulet roti au four",
        ),
        ingredient=Ingredient.objects.create(
            name="Poulet",
            food_type=FoodType.PROTEIN,
            diet_type=DietType.OMNIVORE,
            default_unit=QuantityUnit.GRAM,
            protein_per_100g=Decimal("27.00"),
            carbs_per_100g=Decimal("0.00"),
            fats_per_100g=Decimal("3.60")
        ),
        quantity = 1,
    )

