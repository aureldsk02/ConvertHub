"""
URLs pour l'API des conversions
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.ConversionCategoryViewSet)
router.register(r'types', views.ConversionTypeViewSet)
router.register(r'conversions', views.ConversionViewSet)
router.register(r'file-conversions', views.FileConversionViewSet)

app_name = 'conversions'

urlpatterns = [
    path('', include(router.urls)),
]
