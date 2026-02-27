from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # ==== customisation possible de l'héritage d'affichage page admin
    # list_display = ['email', 'is_staff', 'is_active', ]
    # list_filter = ['is_staff', 'is_active', ]
    # search_fields = ['email', 'first_name', 'last_name', ]
    # ==== customisation possible des champs du formulaire
    # fieldsets = UserAdmin.fieldsets + ('champ_personnel', 'firs_name', 'last_name',')

admin.site.register(CustomUser, CustomUserAdmin)
