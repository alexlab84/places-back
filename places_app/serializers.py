from rest_framework import serializers
from .models import Place

class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
