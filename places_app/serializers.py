from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Place

class PlacesSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  

    class Meta:
        model = Place
        fields = ['id', 'name', 'location', 'category', 'category_display', 'description', 'user']

class UserRegistrationSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Incluye todos los campos necesarios
        extra_kwargs = {
            'password': {'write_only': True}  # Esto asegura que la contraseña no se muestra cuando se consulta
        }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)  # Creamos el usuario
        user.set_password(password)  # Encriptamos la contraseña
        user.save()  # Guardamos el usuario en la base de datos
        return user
    
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        # Usar el método authenticate para verificar las credenciales
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")
        
        return data

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.get(email=email)  # Obtener el usuario por correo

        # Generación de tokens JWT
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }  
    