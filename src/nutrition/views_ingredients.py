from multiprocessing import context

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import Ingredient


# ==== Ingredient CreateView ====
class IngredientsCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "nutrition/user_ingredients_create.html"
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
        context["title"] = "Création d'un ingrédient"
        return context


# ==== Ingredient ListView ====
class IngredientsListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "nutrition/user_ingredients_list.html"
    context_object_name = "ingredients"
    paginate_by = 2

    # def get_queryset(self):
    #     queryset = Ingredient.objects.filter(
    #         user=self.request.user).prefetch_related("ingredients__ingredient")




# ==== Ingredient DetailView ====
class IngredientsDetailView(LoginRequiredMixin, DetailView):
    model = Ingredient
    template_name = "nutrition/user_ingredients_detail.html"
    context_object_name = "ingredient"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = f"Détails de l'ingrédient {context["ingredient"].name}"
        context["title2"] = "Données de la fiche :"
        return context


# ==== Ingredient UpdateView ====
class IngredientsUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "nutrition/user_ingredients_update.html"
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
        context["title"] = "Modification d'un ingrédient"
        return context


# ==== Ingredient DeleteView ====
class IngredientsDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    context_object_name = "ingredient"
    template_name = "nutrition/user_ingredients_delete.html"
    success_url = reverse_lazy("nutrition:ingredients_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression de l'ingrédient"
        return context
