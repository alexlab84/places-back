from django.shortcuts import render


from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Place
from .serializers import  PlacesSerializer


# Lista de lugares
class PlacesList(APIView):
    def get(self, request):
        places = Place.objects.all()
        serializer = PlacesSerializer(places, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PlacesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Detalle de un lugar
class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlacesSerializer

