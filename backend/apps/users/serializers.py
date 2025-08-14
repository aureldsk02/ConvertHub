"""
Sérialiseurs pour l'application users
"""
from rest_framework import serializers
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le profil utilisateur"""
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserStatsSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les statistiques utilisateur"""
    total_conversions = serializers.SerializerMethodField()
    total_file_conversions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'total_conversions', 'total_file_conversions']
        read_only_fields = ['id', 'username', 'total_conversions', 'total_file_conversions']
    
    def get_total_conversions(self, obj):
        return obj.conversions.count()
    
    def get_total_file_conversions(self, obj):
        return obj.file_conversions.count()
