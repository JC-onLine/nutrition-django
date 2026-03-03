from django.urls import path
from .views import profile_view


app_name="accounts"
urlpatterns = [
    # django allauth profile url:
    path("profile/", profile_view, name="profile")
]
