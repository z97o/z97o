from django.db import models
from regions.models import Region

class Tower(models.Model):
    tower_name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='towers')
    signal_strength = models.FloatField()
    status = models.CharField(max_length=50, choices=[
        ('Active', 'Active'),
        ('Maintenance', 'Maintenance'),
        ('Offline', 'Offline'),
    ])
    
    class Meta:
        verbose_name = "Tower"
        verbose_name_plural = "Towers"

    def __str__(self):
        return self.tower_name
