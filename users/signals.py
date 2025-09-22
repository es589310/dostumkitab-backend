from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import UserProfile, Address


@receiver(post_save, sender=UserProfile)
def update_user_profile_search_vector(sender, instance, **kwargs):
    """İstifadəçi profili yaradıldıqda və ya yeniləndikdə search vector yenilə"""
    UserProfile.objects.filter(pk=instance.pk).update(
        search_vector=(
            SearchVector("user__first_name", weight="A") + 
            SearchVector("user__last_name", weight="A") + 
            SearchVector("user__username", weight="B") +
            SearchVector("user__email", weight="C") +
            SearchVector("phone", weight="C") +
            SearchVector("address", weight="D") +
            SearchVector("city", weight="D")
        )
    )


@receiver(post_save, sender=Address)
def update_address_search_vector(sender, instance, **kwargs):
    """Ünvan yaradıldıqda və ya yeniləndikdə search vector yenilə"""
    Address.objects.filter(pk=instance.pk).update(
        search_vector=(
            SearchVector("title", weight="A") + 
            SearchVector("full_address", weight="B") + 
            SearchVector("city", weight="C") +
            SearchVector("district", weight="D") +
            SearchVector("postal_code", weight="E") +
            SearchVector("phone", weight="E")
        )
    )