from django.db import models
from django.utils.text import slugify
from menu33.locations.models import Location


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
        related_name="restaurants"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Automatically generate slug from name
        super().save(*args, **kwargs)

