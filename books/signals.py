from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import Book, Category, Author, Publisher, BookReview, Banner


@receiver(post_save, sender=Book)
def update_book_search_vector(sender, instance, **kwargs):
    """Kitab yaradıldıqda və ya yeniləndikdə search vector yenilə"""
    # Müəllif adlarını topla
    author_names = " ".join([author.name for author in instance.authors.all()])
    
    # Nəşriyyat adı
    publisher_name = instance.publisher.name if instance.publisher else ""
    
    # Kateqoriya adı
    category_name = instance.category.name if instance.category else ""
    
    # Search text yarat
    search_text = f"{instance.title} {instance.description} {author_names} {publisher_name} {category_name}"
    
    # Search vector yarat
    search_vector = SearchVector("search_text", weight="A")
    
    Book.objects.filter(pk=instance.pk).update(
        search_text=search_text,
        search_vector=search_vector
    )


@receiver(post_save, sender=Category)
def update_category_search_vector(sender, instance, **kwargs):
    """Kateqoriya yaradıldıqda və ya yeniləndikdə search vector yenilə"""
    Category.objects.filter(pk=instance.pk).update(
        search_vector=(
            SearchVector("name", weight="A") + 
            SearchVector("description", weight="B")
        )
    )


@receiver(post_save, sender=Author)
def update_author_search_vector(sender, instance, **kwargs):
    """Müəllif yaradıldıqda və ya yeniləndikdə search vector yenilə"""
    Author.objects.filter(pk=instance.pk).update(
        search_vector=(
            SearchVector("name", weight="A") + 
            SearchVector("biography", weight="B") +
            SearchVector("nationality", weight="C")
        )
    )


@receiver(post_save, sender=Publisher)
def update_publisher_search_vector(sender, instance, **kwargs):
    """Nəşriyyat yaradıldıqda və ya yeniləndikdə search vector yenilə"""
    Publisher.objects.filter(pk=instance.pk).update(
        search_vector=(
            SearchVector("name", weight="A") + 
            SearchVector("address", weight="B") +
            SearchVector("email", weight="C")
        )
    )


@receiver(post_save, sender=BookReview)
def update_book_review_search_vector(sender, instance, **kwargs):
    """Kitab rəyi yaradıldıqda və ya yeniləndikdə search vector yenilə"""
    # Rəy yaradıldıqda kitabın search vector-ını yenilə
    Book.objects.filter(pk=instance.book.pk).update(
        search_vector=(
            SearchVector("title", weight="A") + 
            SearchVector("description", weight="B") + 
            SearchVector("authors__name", weight="A") +
            SearchVector("publisher__name", weight="C") +
            SearchVector("category__name", weight="C")
        )
    )


@receiver(post_save, sender=Banner)
def update_banner_search_vector(sender, instance, **kwargs):
    """Banner yaradıldıqda və ya yeniləndikdə search vector yenilə"""
    Banner.objects.filter(pk=instance.pk).update(
        search_vector=(
            SearchVector("title", weight="A") + 
            SearchVector("subtitle", weight="B")
        )
    )


# Müəllif və ya nəşriyyat dəyişəndə kitabların search vector-ını yenilə
@receiver(post_save, sender=Author)
def update_related_books_search_vector(sender, instance, **kwargs):
    """Müəllif dəyişəndə əlaqəli kitabların search vector-ını yenilə"""
    related_books = Book.objects.filter(authors=instance)
    for book in related_books:
        Book.objects.filter(pk=book.pk).update(
            search_vector=(
                SearchVector("title", weight="A") + 
                SearchVector("description", weight="B") + 
                SearchVector("authors__name", weight="A") +
                SearchVector("publisher__name", weight="C") +
                SearchVector("category__name", weight="C")
            )
        )


@receiver(post_save, sender=Publisher)
def update_related_books_publisher_search_vector(sender, instance, **kwargs):
    """Nəşriyyat dəyişəndə əlaqəli kitabların search vector-ını yenilə"""
    related_books = Book.objects.filter(publisher=instance)
    for book in related_books:
        Book.objects.filter(pk=book.pk).update(
            search_vector=(
                SearchVector("title", weight="A") + 
                SearchVector("description", weight="B") + 
                SearchVector("authors__name", weight="A") +
                SearchVector("publisher__name", weight="C") +
                SearchVector("category__name", weight="C")
            )
        )


@receiver(post_save, sender=Category)
def update_related_books_category_search_vector(sender, instance, **kwargs):
    """Kateqoriya dəyişəndə əlaqəli kitabların search vector-ını yenilə"""
    related_books = Book.objects.filter(category=instance)
    for book in related_books:
        Book.objects.filter(pk=book.pk).update(
            search_vector=(
                SearchVector("title", weight="A") + 
                SearchVector("description", weight="B") + 
                SearchVector("authors__name", weight="A") +
                SearchVector("publisher__name", weight="C") +
                SearchVector("category__name", weight="C")
            )
        )