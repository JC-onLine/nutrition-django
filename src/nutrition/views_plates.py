# from allauth.core.internal.httpkit import
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .models import Plate
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

@login_required
def plates_update(request, pk):
    plate = get_object_or_404(Plate, pk=pk, user=request.user)
    # POST method
    if request.method == "POST":
        plate_form = PlateForm(request.POST, instance=plate)
        formset = PlateIngredientFormset(request.POST, queryset=plate.ingredients.all())

        if plate_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                plate_form.save()
                formset.save()
            return redirect(plate)
    else:
        plate_form = PlateForm(instance=plate) # permet de préremplir le formulaire avec la base de données
        formset = PlateIngredientFormset(queryset=plate.ingredients.all())
    return render(
        request, "nutrition/plates_update_form.html", # formulaire composé de plusieurs partials
        context={
            "formset": formset,
            "plate": plate,
            "diet_type_choices": DietType.choices,
            "view_tag": "plates_update",
            "title_tab": f"Modification assiette {plate.name} - Doc Nutrition",
            "title1": f"Modification de l'assiette {plate.name}",
            "title2": "",
            "title3": "",
            "view_debug": VIEW_DEBUG,
        }
    )

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
