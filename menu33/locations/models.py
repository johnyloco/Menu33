from urllib.parse import parse_qs, urlparse

from django.db import models


class Location(models.Model):
    SWISS_CANTONS = [
        ("AG", "Aargau"),
        ("AI", "Appenzell Innerrhoden"),
        ("AR", "Appenzell Ausserrhoden"),
        ("BE", "Bern"),
        ("BL", "Basel-Landschaft"),
        ("BS", "Basel-Stadt"),
        ("FR", "Fribourg"),
        ("GE", "Geneva"),
        ("GL", "Glarus"),
        ("GR", "Graubünden"),
        ("JU", "Jura"),
        ("LU", "Lucerne"),
        ("NE", "Neuchâtel"),
        ("NW", "Nidwalden"),
        ("OW", "Obwalden"),
        ("SG", "St. Gallen"),
        ("SH", "Schaffhausen"),
        ("SO", "Solothurn"),
        ("SZ", "Schwyz"),
        ("TG", "Thurgau"),
        ("TI", "Ticino"),
        ("UR", "Uri"),
        ("VD", "Vaud"),
        ("VS", "Valais"),
        ("ZG", "Zug"),
        ("ZH", "Zurich"),
    ]

    address = models.CharField(max_length=255)
    google_maps = models.URLField(max_length=500, blank=True, null=True)

    def get_embed_url(self):
        if not self.google_maps:
            return None
        if "embed" in self.google_maps:
            return self.google_maps  # Already an embed URL
        # Generate an embed URL from a regular URL
        base_embed_url = "https://www.google.com/maps/embed"
        parsed_url = urlparse(self.google_maps)
        query = parse_qs(parsed_url.query)
        return f"{base_embed_url}?q={query.get('q', [''])[0]}"

    city = models.CharField(max_length=100)
    canton = models.CharField(max_length=2, choices=SWISS_CANTONS)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.get_canton_display()}"
