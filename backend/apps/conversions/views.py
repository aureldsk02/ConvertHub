"""
Vues pour l'API des conversions
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import AnonymousUser

from .models import ConversionCategory, ConversionType, Conversion, FileConversion
from .serializers import (
    ConversionCategorySerializer, ConversionTypeSerializer, 
    ConversionSerializer, FileConversionSerializer,
    ConversionRequestSerializer, FileConversionRequestSerializer
)


class ConversionCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les catégories de conversion"""
    queryset = ConversionCategory.objects.filter(is_active=True)
    serializer_class = ConversionCategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def conversion_types(self, request, slug=None):
        """Récupérer tous les types de conversion d'une catégorie"""
        category = self.get_object()
        conversion_types = category.conversion_types.filter(is_active=True)
        serializer = ConversionTypeSerializer(conversion_types, many=True)
        return Response(serializer.data)


class ConversionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les types de conversion"""
    queryset = ConversionType.objects.filter(is_active=True)
    serializer_class = ConversionTypeSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


class ConversionViewSet(viewsets.ModelViewSet):
    """API pour l'historique des conversions"""
    queryset = Conversion.objects.all()
    serializer_class = ConversionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # Les utilisateurs connectés voient leurs conversions
            queryset = queryset.filter(user=self.request.user)
        else:
            # Les utilisateurs anonymes voient seulement les conversions publiques
            queryset = queryset.filter(user__isnull=True)
        return queryset
    
    def perform_create(self, serializer):
        """Créer une conversion avec les informations de l'utilisateur"""
        # Récupérer l'adresse IP et le user agent
        ip_address = self.get_client_ip()
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        # Définir l'utilisateur (peut être None pour les utilisateurs anonymes)
        user = self.request.user if self.request.user.is_authenticated else None
        
        serializer.save(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def get_client_ip(self):
        """Récupérer l'adresse IP du client"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=False, methods=['post'])
    def convert(self, request):
        """Effectuer une conversion et l'enregistrer"""
        serializer = ConversionRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Récupérer le type de conversion
                conversion_type = ConversionType.objects.get(
                    id=serializer.validated_data['conversion_type_id'],
                    is_active=True
                )
                
                # Effectuer la conversion (logique simplifiée pour l'instant)
                input_value = serializer.validated_data['input_value']
                output_value = self._perform_conversion(
                    input_value,
                    serializer.validated_data['input_unit'],
                    serializer.validated_data['output_unit']
                )
                
                # Créer l'enregistrement de conversion
                conversion_data = {
                    'conversion_type': conversion_type,
                    'input_value': input_value,
                    'output_value': output_value,
                    'input_unit': serializer.validated_data['input_unit'],
                    'output_unit': serializer.validated_data['output_unit'],
                }
                
                conversion_serializer = ConversionSerializer(data=conversion_data)
                if conversion_serializer.is_valid():
                    conversion_serializer.save(
                        user=request.user if request.user.is_authenticated else None,
                        ip_address=self.get_client_ip(),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                    
                    return Response({
                        'success': True,
                        'input_value': input_value,
                        'output_value': output_value,
                        'input_unit': serializer.validated_data['input_unit'],
                        'output_unit': serializer.validated_data['output_unit'],
                        'conversion_id': conversion_serializer.instance.id
                    })
                
            except ConversionType.DoesNotExist:
                return Response(
                    {'error': 'Type de conversion non trouvé'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {'error': f'Erreur lors de la conversion: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _perform_conversion(self, input_value, input_unit, output_unit):
        """Logique de conversion (à implémenter selon les besoins)"""
        # Pour l'instant, retourner une valeur factice
        # Cette logique sera implémentée plus tard avec des algorithmes réels
        return input_value * 1.5  # Exemple simplifié


class FileConversionViewSet(viewsets.ModelViewSet):
    """API pour les conversions de fichiers"""
    queryset = FileConversion.objects.all()
    serializer_class = FileConversionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        else:
            queryset = queryset.filter(user__isnull=True)
        return queryset
    
    def perform_create(self, serializer):
        """Créer une conversion de fichier"""
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user, status='pending')
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Traiter une conversion de fichier"""
        file_conversion = self.get_object()
        
        if file_conversion.status != 'pending':
            return Response(
                {'error': 'Cette conversion ne peut pas être traitée'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Marquer comme en cours de traitement
        file_conversion.status = 'processing'
        file_conversion.save()
        
        try:
            # Ici, on appellera plus tard Celery pour le traitement asynchrone
            # Pour l'instant, simulation d'un traitement
            import time
            time.sleep(1)  # Simulation
            
            # Marquer comme terminé
            file_conversion.status = 'completed'
            file_conversion.completed_at = timezone.now()
            file_conversion.save()
            
            return Response({'status': 'completed'})
            
        except Exception as e:
            file_conversion.status = 'failed'
            file_conversion.error_message = str(e)
            file_conversion.save()
            
            return Response(
                {'error': f'Erreur lors du traitement: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
