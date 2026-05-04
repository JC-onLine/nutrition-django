# from allauth.core.internal.httpkit import
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .models import Plate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlateForm, PlateIngredientFormset
from .choices import DietType


# ==== Plate CreateView ====
class PlatesCreateView(LoginRequiredMixin, CreateView):
    model = Plate
    template_name = "nutrition/user_plates_create.html"
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
        context["title"] = "Création d'une nouvelle assiette"
        return context



# ==== Plate ListView ====
class PlatesListView(LoginRequiredMixin, ListView):
    model = Plate
    template_name = "nutrition/user_plates.html"
    context_object_name = "plates"
    paginate_by = 2

    def get_queryset(self):
        queryset = Plate.objects.filter(
            user=self.request.user).prefetch_related("ingredients__ingredient")

        search_query = self.request.GET.get("search", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(ingredients__ingredient__name__icontains=search_query)).distinct()

        return queryset.order_by("-created_at")

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["nutrition/partials/plates_list.html"]
        return [self.template_name]


# ==== Plate DetailView ====
class PlatesDetailView(LoginRequiredMixin, DetailView):
    model = Plate
    template_name = "nutrition/user_plates_detail.html"
    context_object_name = "plate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Détails de l'assiette"
        return context


# ==== Plate UpdateView ====
# class PlatesUpdateView(LoginRequiredMixin, UpdateView):
#     model = Plate
#     template_name = "nutrition/user_plates_update.html"
#     fields = ["name"]
#
#     def form_valid(self, form):
#         form.instance.name = form.cleaned_data['name']
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse("nutrition:plates_detail",
#                        args=[self.object.pk])
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Modification d'une assiette"
#         return context
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
        plate_form = PlateForm(instance=plate)
        formset = PlateIngredientFormset(queryset=plate.ingredients.all())
    return render(
        request, "nutrition/user_plates_update.html",
        context={
            "formset": formset,
            "plate": plate,
            "diets": DietType.choices,
            "title": "Modification de l'assiette"
        }
    )

# ==== Plate DeleteView ====
class PlatesDeleteView(LoginRequiredMixin, DeleteView):
    model = Plate
    context_object_name = "plate"
    template_name = "nutrition/user_plates_delete.html"
    success_url = reverse_lazy("nutrition:user_plates")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suppression de l'assiette"
        return context
