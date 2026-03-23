from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Plate


# ==== Plate CreateView ====
class PlatesCreateView(LoginRequiredMixin, CreateView):
    ...


# ==== Plate ListView ====
class PlatesListView(LoginRequiredMixin, ListView):
    model = Plate
    template_name = "nutrition/user_plates.html"
    context_object_name = "plates"
    paginate_by = 2

    def get_queryset(self):

        queryset = Plate.objects.filter(user=self.request.user).prefetch_related("ingredients__ingredient")

        search_query = self.request.GET.get("search", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(ingredients__ingredient__name__icontains=search_query)).distinct()

        return queryset

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["nutrition/partials/plates_list.html"]
        return [self.template_name]


# ==== Plate DetailView ====
class PlatesDetailView(LoginRequiredMixin, DetailView):
    ...


# ==== Plate UpdateView ====
class PlatesUpdateView(LoginRequiredMixin, UpdateView):
    ...


# ==== Plate DeleteView ====
class PlatesDeleteView(LoginRequiredMixin, DeleteView):
    ...


