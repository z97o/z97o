# core/models.py
from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Tower(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="towers")
    tower_id = models.CharField(max_length=50, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status = models.CharField(max_length=20, default="Active")

    class Meta:
        ordering = ["tower_id"]

    def __str__(self):
        return self.tower_id


PRIORITY_CHOICES = [
    ("Low", "Low"),
    ("Medium", "Medium"),
    ("High", "High"),
    ("Critical", "Critical"),
]

class Complaint(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    tower = models.ForeignKey(Tower, on_delete=models.SET_NULL, null=True, blank=True)
    customer_msisdn = models.CharField(max_length=20, blank=True)
    category = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="Open")
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.category} - {self.status} - {self.priority or '-'}"
