from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from books.models import Book, Category, Author, Publisher, BookReview, Banner
from users.models import UserProfile, Address
from contact.models import ContactMessage


class Command(BaseCommand):
    help = 'Bütün modellər üçün search vector-ları yenilə'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Yalnız müəyyən model üçün search vector yenilə',
            choices=['book', 'category', 'author', 'publisher', 'userprofile', 'address', 'contactmessage']
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Batch size for processing (default: 1000)'
        )

    def handle(self, *args, **options):
        model_name = options.get('model')
        batch_size = options.get('batch_size')
        
        if model_name:
            self.update_single_model(model_name, batch_size)
        else:
            self.update_all_models(batch_size)

    def update_single_model(self, model_name, batch_size):
        """Tək model üçün search vector yenilə"""
        if model_name == 'book':
            self.update_books(batch_size)
        elif model_name == 'category':
            self.update_categories(batch_size)
        elif model_name == 'author':
            self.update_authors(batch_size)
        elif model_name == 'publisher':
            self.update_publishers(batch_size)
        elif model_name == 'userprofile':
            self.update_user_profiles(batch_size)
        elif model_name == 'address':
            self.update_addresses(batch_size)
        elif model_name == 'contactmessage':
            self.update_contact_messages(batch_size)

    def update_all_models(self, batch_size):
        """Bütün modellər üçün search vector yenilə"""
        self.stdout.write('Bütün modellər üçün search vector-ları yenilənir...')
        
        self.update_books(batch_size)
        self.update_categories(batch_size)
        self.update_authors(batch_size)
        self.update_publishers(batch_size)
        self.update_user_profiles(batch_size)
        self.update_addresses(batch_size)
        self.update_contact_messages(batch_size)
        
        self.stdout.write(
            self.style.SUCCESS('Bütün search vector-lar uğurla yeniləndi!')
        )

    def update_books(self, batch_size):
        """Kitablar üçün search vector yenilə"""
        self.stdout.write('Kitablar üçün search vector yenilənir...')
        
        total_books = Book.objects.count()
        processed = 0
        
        for i in range(0, total_books, batch_size):
            books = Book.objects.all()[i:i + batch_size]
            
            for book in books:
                # Müəllif adlarını topla
                author_names = " ".join([author.name for author in book.authors.all()])
                
                # Nəşriyyat adı
                publisher_name = book.publisher.name if book.publisher else ""
                
                # Kateqoriya adı
                category_name = book.category.name if book.category else ""
                
                # Search text yarat
                search_text = f"{book.title} {book.description} {author_names} {publisher_name} {category_name}"
                
                # Search vector yarat
                search_vector = SearchVector("search_text", weight="A")
                
                Book.objects.filter(pk=book.pk).update(
                    search_text=search_text,
                    search_vector=search_vector
                )
                processed += 1
                
                if processed % 100 == 0:
                    self.stdout.write(f'  {processed}/{total_books} kitab işlənib...')
        
        self.stdout.write(
            self.style.SUCCESS(f'{processed} kitab üçün search vector yeniləndi')
        )

    def update_categories(self, batch_size):
        """Kateqoriyalar üçün search vector yenilə"""
        self.stdout.write('Kateqoriyalar üçün search vector yenilənir...')
        
        total_categories = Category.objects.count()
        processed = 0
        
        for i in range(0, total_categories, batch_size):
            categories = Category.objects.all()[i:i + batch_size]
            
            for category in categories:
                Category.objects.filter(pk=category.pk).update(
                    search_vector=(
                        SearchVector("name", weight="A") + 
                        SearchVector("description", weight="B")
                    )
                )
                processed += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'{processed} kateqoriya üçün search vector yeniləndi')
        )

    def update_authors(self, batch_size):
        """Müəlliflər üçün search vector yenilə"""
        self.stdout.write('Müəlliflər üçün search vector yenilənir...')
        
        total_authors = Author.objects.count()
        processed = 0
        
        for i in range(0, total_authors, batch_size):
            authors = Author.objects.all()[i:i + batch_size]
            
            for author in authors:
                Author.objects.filter(pk=author.pk).update(
                    search_vector=(
                        SearchVector("name", weight="A") + 
                        SearchVector("biography", weight="B") +
                        SearchVector("nationality", weight="C")
                    )
                )
                processed += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'{processed} müəllif üçün search vector yeniləndi')
        )

    def update_publishers(self, batch_size):
        """Nəşriyyatlar üçün search vector yenilə"""
        self.stdout.write('Nəşriyyatlar üçün search vector yenilənir...')
        
        total_publishers = Publisher.objects.count()
        processed = 0
        
        for i in range(0, total_publishers, batch_size):
            publishers = Publisher.objects.all()[i:i + batch_size]
            
            for publisher in publishers:
                Publisher.objects.filter(pk=publisher.pk).update(
                    search_vector=(
                        SearchVector("name", weight="A") + 
                        SearchVector("address", weight="B") +
                        SearchVector("email", weight="C")
                    )
                )
                processed += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'{processed} nəşriyyat üçün search vector yeniləndi')
        )

    def update_user_profiles(self, batch_size):
        """İstifadəçi profilləri üçün search vector yenilə"""
        self.stdout.write('İstifadəçi profilləri üçün search vector yenilənir...')
        
        total_profiles = UserProfile.objects.count()
        processed = 0
        
        for i in range(0, total_profiles, batch_size):
            profiles = UserProfile.objects.all()[i:i + batch_size]
            
            for profile in profiles:
                # Sadə search vector yarat
                search_vector = SearchVector("phone", weight="C") + SearchVector("address", weight="D") + SearchVector("city", weight="D")
                UserProfile.objects.filter(pk=profile.pk).update(search_vector=search_vector)
                processed += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'{processed} istifadəçi profili üçün search vector yeniləndi')
        )

    def update_addresses(self, batch_size):
        """Ünvanlar üçün search vector yenilə"""
        self.stdout.write('Ünvanlar üçün search vector yenilənir...')
        
        total_addresses = Address.objects.count()
        processed = 0
        
        for i in range(0, total_addresses, batch_size):
            addresses = Address.objects.all()[i:i + batch_size]
            
            for address in addresses:
                Address.objects.filter(pk=address.pk).update(
                    search_vector=(
                        SearchVector("title", weight="A") + 
                        SearchVector("full_address", weight="B") + 
                        SearchVector("city", weight="C") +
                        SearchVector("district", weight="D") +
                        SearchVector("postal_code", weight="E") +
                        SearchVector("phone", weight="E")
                    )
                )
                processed += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'{processed} ünvan üçün search vector yeniləndi')
        )

    def update_contact_messages(self, batch_size):
        """Əlaqə mesajları üçün search vector yenilə"""
        self.stdout.write('Əlaqə mesajları üçün search vector yenilənir...')
        
        total_messages = ContactMessage.objects.count()
        processed = 0
        
        for i in range(0, total_messages, batch_size):
            messages = ContactMessage.objects.all()[i:i + batch_size]
            
            for message in messages:
                ContactMessage.objects.filter(pk=message.pk).update(
                    search_vector=(
                        SearchVector("subject", weight="A") + 
                        SearchVector("message", weight="B") + 
                        SearchVector("name", weight="C") +
                        SearchVector("email", weight="D")
                    )
                )
                processed += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'{processed} əlaqə mesajı üçün search vector yeniləndi')
        )