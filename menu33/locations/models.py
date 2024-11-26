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
    city = models.CharField(max_length=100)
    canton = models.CharField(max_length=2, choices=SWISS_CANTONS)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.get_canton_display()}"
