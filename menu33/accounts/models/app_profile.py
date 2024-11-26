from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model() #dynamic way to take the current user model


class Profile(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=40,
        blank=True,
        null=True, #everything is optional
    )

    last_name = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    profile_picture = models.URLField(
        blank=True,
        null=True,
    )

#later to change the URLfield

