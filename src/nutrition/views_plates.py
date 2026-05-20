# from allauth.core.internal.httpkit import
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .models import Plate, Ingredient, PlateIngredient
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlateForm, PlateIngredientFormset
from .choices import DietType

# constantes
VIEW_DEBUG = True

# ==== Plate CreateView ====
class PlatesCreateView(LoginRequiredMixin, CreateView):
    model = Plate
    template_name = "nutrition/plates_create.html"
    fields = ["name"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = form.cleaned_data['name']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("nutrition:plates_detail",
                       args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_tag"] = "PlatesCreateView"
        context["title_tab"] = "Création assiette - Doc Nutrition"
        context["title1"] = "Création d'une assiette"
        context["title2"] = ""
        context["title3"] = ""
        context["view_debug"] = VIEW_DEBUG
        return context


# ==== Plate ListView ====
class PlatesListView(LoginRequiredMixin, ListView):
    model = Plate
    template_name = "nutrition/plates_list_main.html"
    context_object_name = "plates"
    paginate_by = 2

    def get_queryset(self):
        # Filtre sur l'utilisateur
        queryset = Plate.objects.filter(
            user=self.request.user).prefetch_related("ingredients__ingredient")
        # Récupère la clé de recherche depui la barre de recherche
        # "search" est le nom de l'input HTML (strip: suppression des espaces)
        search_query = self.request.GET.get("search", "").strip()
        # Clé de recherche présente
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |   # icontains: ne tiens pas compte de la casse
                Q(ingredients__ingredient__name__icontains=search_query)).distinct() # distinct: supprime les doublons
        return queryset.order_by("-created_at") # trié par date de création

    def get_template_names(self):
        # With HTMX
        if self.request.headers.get("HX-Request"):
            return ["nutrition/partials/plates_list.html"]
        # Without HTMX
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_tag"] = "PlatesListView"
        context["title_tab"] = "Liste assiettes - Doc Nutrition"
        context["title1"] = "Mes assiettes"
        context["title2"] = ""
        context["title3"] = ""
        context["view_debug"] = VIEW_DEBUG
        return context


# ==== Plate DetailView ====
class PlatesDetailView(LoginRequiredMixin, DetailView):
    model = Plate
    template_name = "nutrition/plates_detail.html"
    context_object_name = "plate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Détails de l'assiette"
        context["view_tag"] = "PlatesDetailView"
        context["title_tab"] = f"Détails assiette { context['plate'].name} - Doc Nutrition"
        context["title1"] = f"Détails de l'assiette { context['plate'].name} de { context['plate'].user.username }"
        context["title2"] = ""
        context["title3"] = ""
        context["view_debug"] = VIEW_DEBUG
        return context


# ==== Plate UpdateView ====
class PlatesUpdateView(LoginRequiredMixin, UpdateView):
    model = Plate
    template_name = "nutrition/plates_update.html"
    fields = ["name"]

    def form_valid(self, form):
        form.instance.name = form.cleaned_data['name']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("nutrition:plates_detail",
                       args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_tag"] = "PlatesUpdateView"
        context["title_tab"] = f"Modification assiette {context["plate"].name} - Doc Nutrition"
        context["title1"] = f"Modification de l'assiette {context["plate"].name}"
        context["title2"] = ""
        context["title3"] = ""
        context["view_debug"] = VIEW_DEBUG
        return context

# ==== Plate DeleteView ====
class PlatesDeleteView(LoginRequiredMixin, DeleteView):
    model = Plate
    context_object_name = "plate"
    template_name = "nutrition/plates_delete.html"
    success_url = reverse_lazy("nutrition:plates_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression de l'assiette"
        context["title_tab"] = f"Suppression assiette {context["plate"].name} - Doc Nutrition"
        context["title1"] = f"Suppression de l'assiette {context["plate"].name}"
        context["title2"] = ""
        context["title3"] = ""
        context["view_debug"] = VIEW_DEBUG
        return context


#==== Plates Update function
@login_required
def plates_update(request, pk):
    plate = get_object_or_404(Plate, pk=pk, user=request.user)
    # POST method
    if request.method == "POST":
        plate_form = PlateForm(request.POST, instance=plate)
        formset = PlateIngredientFormset(request.POST, queryset=plate.ingredients.all())
        # validation de 2 formulaires : le nom du plat, ingrédients.
        if plate_form.is_valid() and formset.is_valid():
            # transaction atomic qui permet de sauvegarder la cohérence des 2 tables
            # si bug entre les 2 save(), il y a rollback et rien n'est sauvegardé
            with transaction.atomic():
                plate_form.save()
                formset.save()
            return redirect(plate) # renvoi vers l'objet Plate donc la méthode get_absolute_url, vue de détail
    else:
        plate_form = PlateForm(instance=plate) # permet de préremplir le formulaire avec la base de données
        formset = PlateIngredientFormset(queryset=plate.ingredients.all())
    return render(
        request,
        "nutrition/plates_update_form_htmx.html", # formulaire composé de plusieurs partials
        context={
            "formset": formset,
            "plate": plate,
            "diet_type_choices": DietType.choices,
            "plate_form": plate_form,
            "title_tab": f"Modification assiette {plate.name} - Doc Nutrition",
            "title1": f"Modification de l'assiette {plate.name}",
            "title2": "",
            "title3": "",
        }
    )


#==== Search ingredient with HTMX
@login_required
def ingredients_search(request):
    ingredient_query = request.GET.get('ingredient-query', '').strip() # ingredient_query: search id de l'input HTML
    plate_id = request.GET.get('plate_id', None) # id de l'objet Plate, champ caché id de l'input HTML (type="hidden")
    selected_diet_types = request.GET.getlist('diet_type') # 'list' de checkbox, id groupe HTML
    # au moins 2 caractères de recherche et aucune checkbox
    if len(ingredient_query) < 2 and not selected_diet_types:
        return render(request,
                      "nutrition/partials/ingredient_search_results.html",
                      context={
                          "ingredient": None,
                          "plate_id": plate_id,
                      })
    # cascade de filtres : saisie recherche + selection checkbox
    ingredient = Ingredient.objects.all()
    if len(ingredient_query) >= 2:
        ingredient = ingredient.filter(name__icontains=ingredient_query)
    # plusieurs diet_type possible : [ ]omnivore [x]vegan [x]vegetarian
    if selected_diet_types:
        ingredient = ingredient.filter(diet_type__in=selected_diet_types) # __in: liste de valeurs checkbox
    # exclure les ingrédients déjà dans l'assiétte :
    #   récupère les ids des ingrédients déjà dans les assiettes
    ingredients_ids = PlateIngredient.objects.filter(plate_id=plate_id).values_list('ingredient_id', flat=True)
    ingredients = ingredient.exclude(id__in= ingredients_ids)
    return render(request,
                  "nutrition/partials/ingredient_search_results.html",
                  context={
                      "ingredients": ingredients,
                      "plate_id": plate_id,
                  })


# Add ingredient searched to plate
@login_required
@require_POST
def add_ingredient_to_plate(request, plate_id, ingredient_id):
    plate = get_object_or_404(Plate, pk=plate_id, user=request.user)
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    quantity = request.POST.get(f"quantity-{ingredient_id}", 100) # 100: fallback à 100 au cas ou
    if not PlateIngredient.objects.filter(plate=plate, ingredient=ingredient).exists():
        PlateIngredient.objects.create(plate=plate, ingredient=ingredient, quantity=int(quantity))

    # mise à jour du formset
    formset = PlateIngredientFormset(queryset=plate.ingredients.all())
    return render(request,
                  "nutrition/partials/ingredients_formset.html",
                  context={"formset": formset,}
                  )
