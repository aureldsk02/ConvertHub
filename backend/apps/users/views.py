"""
Vues pour l'application users
"""
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserProfileSerializer, UserStatsSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Vue pour le profil utilisateur"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserStatsView(generics.RetrieveAPIView):
    """Vue pour les statistiques utilisateur"""
    serializer_class = UserStatsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
