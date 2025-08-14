"""
Modèles pour les conversions dans ConvertHub
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ConversionCategory(models.Model):
    """Catégorie de conversion (ex: unités, devises, formats)"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icône")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        verbose_name = "Catégorie de conversion"
        verbose_name_plural = "Catégories de conversion"
        ordering = ['name']

    def __str__(self):
        return self.name


class ConversionType(models.Model):
    """Type de conversion spécifique (ex: température, longueur)"""
    category = models.ForeignKey(
        ConversionCategory, 
        on_delete=models.CASCADE, 
        related_name='conversion_types',
        verbose_name="Catégorie"
    )
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    input_unit = models.CharField(max_length=50, verbose_name="Unité d'entrée")
    output_unit = models.CharField(max_length=50, verbose_name="Unité de sortie")
    formula = models.TextField(blank=True, verbose_name="Formule de conversion")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        verbose_name = "Type de conversion"
        verbose_name_plural = "Types de conversion"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.input_unit} → {self.output_unit})"


class Conversion(models.Model):
    """Historique des conversions effectuées"""
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='conversions',
        verbose_name="Utilisateur"
    )
    conversion_type = models.ForeignKey(
        ConversionType,
        on_delete=models.CASCADE,
        related_name='conversions',
        verbose_name="Type de conversion"
    )
    input_value = models.DecimalField(
        max_digits=20, 
        decimal_places=10, 
        verbose_name="Valeur d'entrée"
    )
    output_value = models.DecimalField(
        max_digits=20, 
        decimal_places=10, 
        verbose_name="Valeur de sortie"
    )
    input_unit = models.CharField(max_length=50, verbose_name="Unité d'entrée")
    output_unit = models.CharField(max_length=50, verbose_name="Unité de sortie")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Adresse IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    class Meta:
        verbose_name = "Conversion"
        verbose_name_plural = "Conversions"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.input_value} {self.input_unit} → {self.output_value} {self.output_unit}"


class FileConversion(models.Model):
    """Conversion de fichiers (images, documents, etc.)"""
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='file_conversions',
        verbose_name="Utilisateur"
    )
    input_file = models.FileField(upload_to='conversions/input/', verbose_name="Fichier d'entrée")
    output_file = models.FileField(upload_to='conversions/output/', verbose_name="Fichier de sortie")
    input_format = models.CharField(max_length=20, verbose_name="Format d'entrée")
    output_format = models.CharField(max_length=20, verbose_name="Format de sortie")
    file_size_input = models.BigIntegerField(verbose_name="Taille fichier entrée (bytes)")
    file_size_output = models.BigIntegerField(verbose_name="Taille fichier sortie (bytes)")
    conversion_time = models.FloatField(verbose_name="Temps de conversion (secondes)")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'En attente'),
            ('processing', 'En cours'),
            ('completed', 'Terminé'),
            ('failed', 'Échoué'),
        ],
        default='pending',
        verbose_name="Statut"
    )
    error_message = models.TextField(blank=True, verbose_name="Message d'erreur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Terminé le")

    class Meta:
        verbose_name = "Conversion de fichier"
        verbose_name_plural = "Conversions de fichiers"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.input_format} → {self.output_format} ({self.status})"
