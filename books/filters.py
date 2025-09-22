import django_filters
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from rest_framework.filters import BaseFilterBackend
from .models import Book, Category


class BookFilter(django_filters.FilterSet):
    """Kitab filtri"""
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.filter(is_active=True))
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    language = django_filters.ChoiceFilter(choices=Book.LANGUAGE_CHOICES)
    is_featured = django_filters.BooleanFilter()
    is_bestseller = django_filters.BooleanFilter()
    is_new = django_filters.BooleanFilter()
    
    class Meta:
        model = Book
        fields = ['category', 'language', 'is_featured', 'is_bestseller', 'is_new']


class FullTextSearchFilter(BaseFilterBackend):
    """
    PostgreSQL Full-Text Search Filter
    DRF SearchFilter əvəzinə istifadə edilir
    """
    
    def filter_queryset(self, request, queryset, view):
        search_term = request.query_params.get('search')
        if not search_term:
            return queryset
        
        # Əgər Book modeli isə, bütün sahələrdə axtarış et
        if queryset.model == Book:
            return queryset.filter(
                Q(search_text__icontains=search_term) |
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(authors__name__icontains=search_term) |
                Q(publisher__name__icontains=search_term) |
                Q(category__name__icontains=search_term)
            ).distinct()
        
        # Digər modellər üçün sadə ILIKE axtarış
        if hasattr(queryset.model, 'title'):
            return queryset.filter(title__icontains=search_term)
        elif hasattr(queryset.model, 'name'):
            return queryset.filter(name__icontains=search_term)
        
        return queryset
    
    def _get_search_vector_for_model(self, model):
        """Model üçün uyğun SearchVector qaytarır"""
        from .models import Book, Category, Author, Publisher
        from users.models import UserProfile, Address
        from contact.models import ContactMessage
        
        if model == Book:
            return (
                SearchVector("title", weight="A") + 
                SearchVector("description", weight="B") + 
                SearchVector("authors__name", weight="A") +
                SearchVector("publisher__name", weight="C") +
                SearchVector("category__name", weight="C")
            )
        elif model == Category:
            return (
                SearchVector("name", weight="A") + 
                SearchVector("description", weight="B")
            )
        elif model == Author:
            return (
                SearchVector("name", weight="A") + 
                SearchVector("biography", weight="B") +
                SearchVector("nationality", weight="C")
            )
        elif model == Publisher:
            return (
                SearchVector("name", weight="A") + 
                SearchVector("address", weight="B") +
                SearchVector("email", weight="C")
            )
        elif model == UserProfile:
            return (
                SearchVector("user__first_name", weight="A") + 
                SearchVector("user__last_name", weight="A") + 
                SearchVector("user__username", weight="B") +
                SearchVector("user__email", weight="C") +
                SearchVector("phone", weight="C") +
                SearchVector("address", weight="D") +
                SearchVector("city", weight="D")
            )
        elif model == Address:
            return (
                SearchVector("title", weight="A") + 
                SearchVector("full_address", weight="B") + 
                SearchVector("city", weight="C") +
                SearchVector("district", weight="D") +
                SearchVector("postal_code", weight="E") +
                SearchVector("phone", weight="E")
            )
        elif model == ContactMessage:
            return (
                SearchVector("subject", weight="A") + 
                SearchVector("message", weight="B") + 
                SearchVector("name", weight="C") +
                SearchVector("email", weight="D")
            )
        
        return None


class AdvancedSearchFilter(BaseFilterBackend):
    """
    Gelişmiş axtarış filter-i
    Fuzzy search, phrase search və digər xüsusiyyətlər
    """
    
    def filter_queryset(self, request, queryset, view):
        search_term = request.query_params.get('search')
        search_type = request.query_params.get('search_type', 'full_text')
        
        if not search_term:
            return queryset
        
        if search_type == 'fuzzy':
            return self._fuzzy_search(queryset, search_term)
        elif search_type == 'phrase':
            return self._phrase_search(queryset, search_term)
        elif search_type == 'prefix':
            return self._prefix_search(queryset, search_term)
        else:
            # Default full-text search
            return self._full_text_search(queryset, search_term)
    
    def _full_text_search(self, queryset, search_term):
        """Full-text search"""
        search_query = SearchQuery(search_term, config='turkish')
        
        if hasattr(queryset.model, 'search_vector'):
            return queryset.annotate(
                rank=SearchRank('search_vector', search_query)
            ).filter(
                search_vector=search_query
            ).order_by('-rank')
        
        return queryset
    
    def _fuzzy_search(self, queryset, search_term):
        """Fuzzy search - səhv yazılan sözləri tapır"""
        from django.contrib.postgres.search import TrigramSimilarity
        
        # Trigram similarity ilə fuzzy search
        if hasattr(queryset.model, 'title'):
            return queryset.annotate(
                similarity=TrigramSimilarity('title', search_term)
            ).filter(
                similarity__gt=0.1
            ).order_by('-similarity')
        
        return queryset
    
    def _phrase_search(self, queryset, search_term):
        """Phrase search - dəqiq ifadə axtarışı"""
        # Phrase search üçün tırnak işarələri əlavə et
        phrase_query = f'"{search_term}"'
        search_query = SearchQuery(phrase_query, config='turkish')
        
        if hasattr(queryset.model, 'search_vector'):
            return queryset.annotate(
                rank=SearchRank('search_vector', search_query)
            ).filter(
                search_vector=search_query
            ).order_by('-rank')
        
        return queryset
    
    def _prefix_search(self, queryset, search_term):
        """Prefix search - söz başlanğıcı axtarışı"""
        # Prefix search üçün * əlavə et
        prefix_query = f'{search_term}*'
        search_query = SearchQuery(prefix_query, config='turkish')
        
        if hasattr(queryset.model, 'search_vector'):
            return queryset.annotate(
                rank=SearchRank('search_vector', search_query)
            ).filter(
                search_vector=search_query
            ).order_by('-rank')
        
        return queryset