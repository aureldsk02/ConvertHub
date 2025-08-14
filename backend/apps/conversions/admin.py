"""
Interface d'administration pour les conversions
"""
from django.contrib import admin
from .models import ConversionCategory, ConversionType, Conversion, FileConversion


@admin.register(ConversionCategory)
class ConversionCategoryAdmin(admin.ModelAdmin):
    """Administration des catégories de conversion"""
    list_display = ['name', 'slug', 'is_active', 'conversion_types_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    def conversion_types_count(self, obj):
        return obj.conversion_types.filter(is_active=True).count()
    conversion_types_count.short_description = 'Types de conversion'


@admin.register(ConversionType)
class ConversionTypeAdmin(admin.ModelAdmin):
    """Administration des types de conversion"""
    list_display = ['name', 'category', 'input_unit', 'output_unit', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'input_unit', 'output_unit']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    """Administration de l'historique des conversions"""
    list_display = ['id', 'user', 'conversion_type', 'input_value', 'output_value', 'created_at']
    list_filter = ['conversion_type__category', 'created_at', 'user']
    search_fields = ['user__username', 'conversion_type__name']
    readonly_fields = ['created_at', 'ip_address', 'user_agent']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        """Les conversions sont créées automatiquement via l'API"""
        return False


@admin.register(FileConversion)
class FileConversionAdmin(admin.ModelAdmin):
    """Administration des conversions de fichiers"""
    list_display = ['id', 'user', 'input_format', 'output_format', 'status', 'created_at']
    list_filter = ['status', 'input_format', 'output_format', 'created_at']
    search_fields = ['user__username', 'input_format', 'output_format']
    readonly_fields = ['created_at', 'completed_at', 'file_size_input', 'file_size_output']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'input_file', 'output_file', 'status')
        }),
        ('Formats', {
            'fields': ('input_format', 'output_format')
        }),
        ('Métadonnées', {
            'fields': ('file_size_input', 'file_size_output', 'conversion_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
        ('Erreurs', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )
