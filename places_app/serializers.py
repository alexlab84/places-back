from rest_framework import serializers
from .models import Place

class PlacesSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Place
        fields = ['id', 'name', 'location', 'category', 'category_display', 'description']
