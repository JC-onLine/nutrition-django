from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse

from .models import Plate


# ==== Plate CreateView ====
class PlatesCreateView(LoginRequiredMixin, CreateView):
    model = Plate
    template_name = "nutrition/user_plates_create.html"
    fields = ["name"]

    def form_valid(self, form):
        form.instance.name = form.cleaned_data['name']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("nutrition:user_plates_detail",
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
    model = Plate
    template_name = "nutrition/user_plates_detail.html"
    context_object_name = "plate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Détails de l'assiette"
        return context


# ==== Plate UpdateView ====
class PlatesUpdateView(LoginRequiredMixin, UpdateView):
    ...


# ==== Plate DeleteView ====
class PlatesDeleteView(LoginRequiredMixin, DeleteView):
    ...


