from django.shortcuts import render

from django.contrib.auth import authenticate
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.tokens import RefreshToken  # Para crear el token JWT
from .models import Place
from .serializers import PlacesSerializer, UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny




class PlacesList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        places = Place.objects.filter(user=request.user)
        serializer = PlacesSerializer(places, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PlacesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Place.objects.all()
    serializer_class = PlacesSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)  
        refresh_token = str(refresh)

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,  
            'user': serializer.data,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]  
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email)
        print(password)
        
        user = User.objects.filter(email=email).first()

        
        if not user:
            return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        
        user = authenticate(username=user.username, password=password)

        if not user:
            return Response({"detail": "Contraseña incorrecta."}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        
        return Response({
            "access": access_token,
            "refresh": str(refresh)  
        }, status=status.HTTP_200_OK)
