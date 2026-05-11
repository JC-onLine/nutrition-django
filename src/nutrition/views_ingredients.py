from typing import Any
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Ingredient
from .forms import IngredientForm, PlateIngredientFormset
from .choices import DietType

# constantes
VIEW_DEBUG = False

# ==== Ingredient CreateView ====
class IngredientsCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "nutrition/nutrition.html"
    fields = ["name", "food_type", "diet_type", "default_unit",
              "protein_per_100g", "carbs_per_100g", "fats_per_100g",
              "average_piece_weight",]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = form.cleaned_data['name']
        form.instance.food_type = form.cleaned_data['food_type']
        form.instance.diet_type = form.cleaned_data['diet_type']
        form.instance.default_unit = form.cleaned_data['default_unit']
        form.instance.protein_per_100g = form.cleaned_data['protein_per_100g']
        form.instance.carbs_per_100g = form.cleaned_data['carbs_per_100g']
        form.instance.fats_per_100g = form.cleaned_data['fats_per_100g']
        form.instance.average_piece_weight = form.cleaned_data['average_piece_weight']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("nutrition:ingredients_detail",
                       args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_tag"] = "IngredientsCreateView"
        context["title_tab"] = "Ajout ingrédients - Doc Nutrition"
        context["title1"] = "Ajout d'un ingrédient"
        context["title2"] = ""
        context["title3"] = ""
        context["view_debug"] = VIEW_DEBUG
        return context


# ==== Ingredient ListView ====
class IngredientsListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "nutrition/nutrition.html"
    context_object_name = "ingredients"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_tag"] = "IngredientsListView"
        context["title_tab"] = "Liste ingrédients - Doc Nutrition"
        context["title1"] = "Mes ingrédients"
        context["title2"] = ""
        context["title3"] = ""
        context["view_debug"] = VIEW_DEBUG
        return context

    # def get_queryset(self):
    #     queryset = Ingredient.objects.filter(
    #         user=self.request.user).prefetch_related("ingredients__ingredient")


# ==== Ingredient DetailView ====
class IngredientsDetailView(LoginRequiredMixin, DetailView):
    model = Ingredient
    template_name = "nutrition/nutrition.html"
    context_object_name = "ingredient"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_tag"] = "IngredientsDetailView"
        context["title_tab"] = f"Détails ingrédient {context["ingredient"].name} - Doc Nutrition"
        context["title1"] = f"Détails de l'ingrédient {context["ingredient"].name}"
        context["title2"] = ""
        context["title3"] = ""
        context["view_debug"] = VIEW_DEBUG
        return context


# ==== Ingredient UpdateView ====
class IngredientsUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "nutrition/nutrition.html"
    fields = ["name", "food_type", "diet_type", "default_unit",
              "protein_per_100g", "carbs_per_100g", "fats_per_100g",
              "average_piece_weight",]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = form.cleaned_data['name']
        form.instance.food_type = form.cleaned_data['food_type']
        form.instance.diet_type = form.cleaned_data['diet_type']
        form.instance.default_unit = form.cleaned_data['default_unit']
        form.instance.protein_per_100g = form.cleaned_data['protein_per_100g']
        form.instance.carbs_per_100g = form.cleaned_data['carbs_per_100g']
        form.instance.fats_per_100g = form.cleaned_data['fats_per_100g']
        form.instance.average_piece_weight = form.cleaned_data['average_piece_weight']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("nutrition:ingredients_detail",
                       args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_tag"] = "IngredientsUpdateView"
        context["title_tab"] = f"Modification ingrédient {context["ingredient"].name} - Doc Nutrition"
        context["title1"] = f"Modification de l'ingrédient {context["ingredient"].name}"
        context["title2"] = ""
        context["title3"] = ""
        context["view_debug"] = VIEW_DEBUG
        return context


# ==== Ingredient DeleteView ====
class IngredientsDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    context_object_name = "ingredient"
    template_name = "nutrition/nutrition.html"
    success_url = reverse_lazy("nutrition:ingredients_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_tag"] = "IngredientsDeleteView"
        context["title_tab"] = f"Suppression ingrédient {context["ingredient"].name} - Doc title_tab"
        context["title1"] = f"Suppression de l'ingrédient {context["ingredient"].name}"
        context["title2"] = ""
        context["title3"] = ""
        context["view_debug"] = VIEW_DEBUG
        return context
