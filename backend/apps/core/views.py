"""
Vues pour l'application core
"""
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count
from apps.conversions.models import Conversion, FileConversion, ConversionCategory


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """Vérification de l'état de l'API"""
    return Response({
        'status': 'healthy',
        'message': 'ConvertHub API is running',
        'timestamp': '2024-01-01T00:00:00Z'
    })


class GlobalStatsView(generics.RetrieveAPIView):
    """Vue pour les statistiques globales"""
    permission_classes = [permissions.AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        """Récupérer les statistiques globales"""
        total_conversions = Conversion.objects.count()
        total_file_conversions = FileConversion.objects.count()
        total_categories = ConversionCategory.objects.filter(is_active=True).count()
        
        # Statistiques par catégorie
        category_stats = ConversionCategory.objects.filter(
            is_active=True
        ).annotate(
            conversion_count=Count('conversion_types__conversions')
        ).values('name', 'conversion_count')
        
        return Response({
            'total_conversions': total_conversions,
            'total_file_conversions': total_file_conversions,
            'total_categories': total_categories,
            'category_stats': list(category_stats),
            'last_updated': '2024-01-01T00:00:00Z'
        })
