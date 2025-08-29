from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import SiteSettings, Logo
from .serializers import SiteSettingsSerializer, LogoSerializer
from lib.serializer_cache import SerializerCacheManager

class SiteSettingsView(RetrieveAPIView):
    """Sayt tənzimləmələri"""
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        # Cache key
        cache_key = 'site_settings'
        
        # Cache-dən al
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Database-dən al
        settings = SiteSettings.get_settings()
        
        # Cache-ə yaz (5 dəqiqə)
        cache.set(cache_key, settings, 300)
        
        return settings
    
    def get_serializer(self, *args, **kwargs):
        # Serializer cache-dən al
        cached_serializer = SerializerCacheManager.get_cached_serializer(
            self.serializer_class, 
            args, 
            kwargs
        )
        
        if cached_serializer:
            return cached_serializer
        
        # Yeni serializer yarad və cache et
        return SerializerCacheManager.cache_serializer(
            self.serializer_class, 
            args, 
            kwargs
        )

@api_view(['GET'])
def whatsapp_number(request):
    """WhatsApp nömrəsini qaytarır"""
    # Cache key
    cache_key = 'whatsapp_number'
    
    # Cache-dən al
    cached_number = cache.get(cache_key)
    if cached_number:
        return Response({
            'whatsapp_number': cached_number
        })
    
    # Database-dən al
    settings = SiteSettings.get_settings()
    
    # Cache-ə yaz (10 dəqiqə)
    cache.set(cache_key, settings.whatsapp_number, 600)
    
    return Response({
        'whatsapp_number': settings.whatsapp_number
    })

class LogoView(RetrieveAPIView):
    """Logo tənzimləmələri"""
    serializer_class = LogoSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        # Cache key
        cache_key = 'logo_settings'
        
        # Cache-dən al
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Database-dən al
        logo = Logo.get_settings()
        
        # Cache-ə yaz (5 dəqiqə)
        cache.set(cache_key, logo, 300)
        
        return logo
    
    def get_serializer(self, *args, **kwargs):
        # Serializer cache-dən al
        cached_serializer = SerializerCacheManager.get_cached_serializer(
            self.serializer_class, 
            args, 
            kwargs
        )
        
        if cached_serializer:
            return cached_serializer
        
        # Yeni serializer yarad və cache et
        return SerializerCacheManager.cache_serializer(
            self.serializer_class, 
            args, 
            kwargs
        )
