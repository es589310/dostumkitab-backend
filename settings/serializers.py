from rest_framework import serializers
from .models import SiteSettings, Logo

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_description', 'phone', 'email', 
            'address', 'working_hours', 'copyright_year', 'whatsapp_number',
            'coordinates', 'navbar_logo', 'navbar_logo_imagekit_url', 
            'footer_logo', 'footer_logo_imagekit_url'
        ]


class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = [
            'site_name', 'navbar_logo', 'navbar_logo_imagekit_url',
            'footer_logo', 'footer_logo_imagekit_url', 'is_active'
        ] 