from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.validators import LETTER_SPACE_DASH_VALIDATOR


class CustomManager(BaseUserManager):
    def create_user(self, username, email, password, **kwargs):
        if not username:
            raise ValueError("Le nom est obligatoire")
        if not email:
            raise ValueError("L'email est obligatoire")

        user = self.model(username=username,
                          email=BaseUserManager.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if not kwargs.get("is_staff"):
            raise ValueError("Le superuser doit avoir is_staff=True.")
        if not kwargs.get("is_superuser"):
            raise ValueError("Le superuser doit avoir is_superuser=True.")

        return self.create_user(username, email, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # IntegrityError
    first_name = models.CharField(max_length=150, verbose_name="Prénom",
                                  validators=[LETTER_SPACE_DASH_VALIDATOR])
    last_name = models.CharField(max_length=150, verbose_name="Nom",
                                 validators=[LETTER_SPACE_DASH_VALIDATOR])
    objects = CustomManager()

