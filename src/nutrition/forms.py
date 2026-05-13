from django import forms
from .models import Plate, PlateIngredient, Ingredient


class PlateForm(forms.ModelForm):
    class Meta:
        model = Plate
        fields = ["name"]

PlateIngredientFormset = forms.modelformset_factory(
    PlateIngredient,
    fields = ["ingredient", "quantity"], # Ajoutez les champs que vous souhaitez afficher
    extra = 0, # si égale 1, ajoute une ligne préremplie
    can_delete=True, # permet de supprimer une ligne avec une checkbox
)

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"

