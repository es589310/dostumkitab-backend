from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import ContactMessage


@receiver(post_save, sender=ContactMessage)
def update_contact_message_search_vector(sender, instance, **kwargs):
    """Əlaqə mesajı yaradıldıqda və ya yeniləndikdə search vector yenilə"""
    ContactMessage.objects.filter(pk=instance.pk).update(
        search_vector=(
            SearchVector("subject", weight="A") + 
            SearchVector("message", weight="B") + 
            SearchVector("name", weight="C") +
            SearchVector("email", weight="D")
        )
    )