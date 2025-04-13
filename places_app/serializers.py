from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Place
import re

class PlacesSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  

    class Meta:
        model = Place
        fields = ['id', 'name', 'location', 'category', 'category_display', 'description', 'user']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']  
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def validate_email(self, value):
        """Verifica que el email no esté ya registrado"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.get('email')

        base_username = re.sub(r'\W+', '', email.split('@')[0])  
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User(username=username, email=email)
        user.set_password(password)  
        user.save()  
        return user
    
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas")

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")

        
        return data

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.get(email=email)  
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }  
    