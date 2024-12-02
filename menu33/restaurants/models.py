from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from menu33.locations.models import Location

UserModel = get_user_model()


class Restaurant(models.Model):
    name = models.CharField(
        max_length=255,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )  # Slug field
    description = models.TextField()
    image = models.URLField(max_length=500, blank=True, null=True)  # Image field as URL
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,  # Delete the restaurant if the associated location is deleted
        related_name="restaurants",
        null=False,
    )
    address = models.CharField(max_length=255)
    google_maps = models.URLField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100)
    canton = models.CharField(max_length=2, choices=Location.SWISS_CANTONS)

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Automatically generate slug from name
        super().save(*args, **kwargs)

