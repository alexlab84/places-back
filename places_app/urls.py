from django.urls import path
from . import views

urlpatterns = [
    path('places/', views.PlacesList.as_view(), name='place-list'),  # Obtener todos los lugares y crear
    path('places/<int:pk>/', views.PlaceDetail.as_view(), name='place-detail'),  # Detalles, actualizar, eliminar
]