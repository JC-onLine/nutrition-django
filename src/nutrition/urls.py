from django.urls import path
from .views import PlatesListView, PlatesCreateView, PlatesDetailView, PlatesUpdateView, PlatesDeleteView


app_name = "nutrition"
urlpatterns = [
    # ==== Plate CRUD ====
    path("plates/create", PlatesCreateView.as_view(), name="plates_create"),
    path("user-plates", PlatesListView.as_view(), name="user_plates"),
    path('plates/detail/<int:pk>/', PlatesDetailView.as_view(), name='plates_detail'),
    path('plates/update/<int:pk>/', PlatesUpdateView.as_view(), name='plates_update'),
    path('plates/delete/<int:pk>/', PlatesDeleteView.as_view(), name='plates_delete'),

]
