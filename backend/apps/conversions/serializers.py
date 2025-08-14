"""
Sérialiseurs pour l'API des conversions
"""
from rest_framework import serializers
from .models import ConversionCategory, ConversionType, Conversion, FileConversion


class ConversionCategorySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les catégories de conversion"""
    conversion_types_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ConversionCategory
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 
            'is_active', 'conversion_types_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_conversion_types_count(self, obj):
        return obj.conversion_types.filter(is_active=True).count()


class ConversionTypeSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les types de conversion"""
    category = ConversionCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ConversionType
        fields = [
            'id', 'category', 'category_id', 'name', 'slug', 'description',
            'input_unit', 'output_unit', 'formula', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConversionSerializer(serializers.ModelSerializer):
    """Sérialiseur pour l'historique des conversions"""
    conversion_type = ConversionTypeSerializer(read_only=True)
    conversion_type_id = serializers.IntegerField(write_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Conversion
        fields = [
            'id', 'user', 'conversion_type', 'conversion_type_id',
            'input_value', 'output_value', 'input_unit', 'output_unit',
            'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'ip_address', 'user_agent', 'created_at']


class FileConversionSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les conversions de fichiers"""
    user = serializers.ReadOnlyField(source='user.username')
    input_file_url = serializers.SerializerMethodField()
    output_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FileConversion
        fields = [
            'id', 'user', 'input_file', 'output_file', 'input_file_url',
            'output_file_url', 'input_format', 'output_format',
            'file_size_input', 'file_size_output', 'conversion_time',
            'status', 'error_message', 'created_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'user', 'output_file', 'file_size_input', 'file_size_output',
            'conversion_time', 'status', 'error_message', 'created_at', 'completed_at'
        ]
    
    def get_input_file_url(self, obj):
        if obj.input_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.input_file.url)
        return None
    
    def get_output_file_url(self, obj):
        if obj.output_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.output_file.url)
        return None


class ConversionRequestSerializer(serializers.Serializer):
    """Sérialiseur pour les requêtes de conversion"""
    conversion_type_id = serializers.IntegerField(required=True)
    input_value = serializers.DecimalField(max_digits=20, decimal_places=10, required=True)
    input_unit = serializers.CharField(max_length=50, required=True)
    output_unit = serializers.CharField(max_length=50, required=True)


class FileConversionRequestSerializer(serializers.Serializer):
    """Sérialiseur pour les requêtes de conversion de fichiers"""
    input_file = serializers.FileField(required=True)
    output_format = serializers.CharField(max_length=20, required=True)
