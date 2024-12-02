from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from menu33.restaurants.models import Restaurant

YEAR_CHOICES = [(year, year) for year in range(1900, datetime.now().year + 1)]
SECTION_CHOICES = (
    ('Starters', 'Starters'),
    ('Main Course', 'Main Course'),
    ('Desserts', 'Desserts'),
    ('Other', 'Other'),
)

UserModel = get_user_model()


class FoodItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE,
        related_name="food_items"
    )
    name = models.CharField(
        max_length=255,
    )
    section = models.CharField(
        max_length=20,
        choices=SECTION_CHOICES,
        default='Other'
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    gluten_free = models.BooleanField(
        default=False,
    )
    dairy_free = models.BooleanField(
        default=False,
    )
    vegan = models.BooleanField(
        default=False,
    )
    image = models.URLField(
        max_length=500,
        blank=True,
        null=True,
    )

    slug = models.SlugField(null=True, unique=True, blank=True)

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DrinkItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="drink_items"
    )
    name = models.CharField(
        max_length=50,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    image = models.URLField(
        max_length=500,
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        null=True,
        unique=True,
        blank=True,
    )

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class WineItem(models.Model):
    class WineType(models.TextChoices):
        RED = 'RED', 'Red'
        WHITE = 'WHITE', 'White'
        ROSE = 'ROSE', 'Rosé'
        SPARKLING = 'SPARKLING', 'Sparkling'
        DESSERT = 'DESSERT', 'Dessert'
        FORTIFIED = 'FORTIFIED', 'Fortified'

    restaurants = models.ManyToManyField(
        'restaurants.Restaurant',
        related_name="wine_items"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    wine_type = models.CharField(
        max_length=50,
        choices=WineType.choices,
        blank=True,
        null=True
    )
    region = models.CharField(max_length=100, blank=True, null=True)
    grape_variety = models.CharField(max_length=100, blank=True, null=True)
    vintage = models.IntegerField(
        choices=YEAR_CHOICES,
        blank=True,
        null=True
    )
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.URLField(max_length=500, blank=True, null=True)
    slug = models.SlugField(null=True, unique=True, blank=True)

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
