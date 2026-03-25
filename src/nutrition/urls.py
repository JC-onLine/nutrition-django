from django.urls import path
from .views_plates import PlatesListView, PlatesCreateView, PlatesDetailView, PlatesUpdateView, PlatesDeleteView
from .views_ingredients import IngredientsCreateView, IngredientsDetailView, IngredientsListView

app_name = "nutrition"
urlpatterns = [
    # ==== Plate CRUD ====
    path("plates/create", PlatesCreateView.as_view(), name="plates_create"),
    path("user-plates", PlatesListView.as_view(), name="user_plates"),
    path('plates/detail/<int:pk>/', PlatesDetailView.as_view(), name='plates_detail'),
    path('plates/update/<int:pk>/', PlatesUpdateView.as_view(), name='plates_update'),
    path('plates/delete/<int:pk>/', PlatesDeleteView.as_view(), name='plates_delete'),
    # ==== Ingredient CRUD ====
    path("ingredients/create", IngredientsCreateView.as_view(), name="ingredients_create"),
    path("ingredients/list", IngredientsListView.as_view(), name="ingredients_list"),
    path('ingredients/detail/<int:pk>/', IngredientsDetailView.as_view(), name='ingredients_detail'),

]
