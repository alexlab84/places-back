from django.urls import path, include
from django.contrib import admin
from . import views
from .views import UserRegistrationView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('places/', views.PlacesList.as_view(), name='place-list'),
    path('places/<int:pk>/', views.PlaceDetail.as_view(), name='place-detail'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]