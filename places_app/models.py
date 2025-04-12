from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('bar', 'Bar'),
        ('restaurant', 'Restaurante'),
        ('museum', 'Museo'),
        ('park', 'Parque'),
        ('shopping_center', 'Centro Comercial'),
        ('kids_zone', 'Zona de Juegos para Niños'),
        ('cinema', 'Cine'),
        ('beach', 'Playa'),
        ('mountain', 'Montaña'),
        ('city', 'Ciudad'),
        ('nature', 'Naturaleza'),
        ('hotel', 'Hotel'),
        ('other', 'Otro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='places')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    


    def __str__(self):
        return self.name
