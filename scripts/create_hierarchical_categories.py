#!/usr/bin/env python3
"""
3 mərhələli kateqoriya strukturu yaradır
Kitab → Tarix → Osmanlı Tarixi
"""

import os
import sys
import django

# Django setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitab_backend.settings')
django.setup()

from books.models import Category

def create_hierarchical_categories():
    """3 mərhələli kateqoriya strukturu yaradır"""
    
    print("3 mərhələli kateqoriya strukturu yaradılır...")
    
    # 1-ci mərhələ - Ana kateqoriyalar
    main_categories = [
        {'name': 'Kitab', 'slug': 'kitab', 'order': 1},
        {'name': 'Dergi', 'slug': 'dergi', 'order': 2},
        {'name': 'Takvim', 'slug': 'takvim', 'order': 3},
        {'name': 'Çocuklara Özel', 'slug': 'cocuklara-ozel', 'order': 4},
        {'name': 'Zeka Oyunları', 'slug': 'zeka-oyunlari', 'order': 5},
        {'name': 'Dini Malzemeler', 'slug': 'dini-malzemeler', 'order': 6},
        {'name': 'Kırtasiye', 'slug': 'kirtasiye', 'order': 7},
    ]
    
    # 2-ci mərhələ - Alt kateqoriyalar
    sub_categories = {
        'Kitab': [
            {'name': 'Tarih', 'slug': 'tarih', 'order': 1},
            {'name': 'Edebiyat', 'slug': 'edebiyat', 'order': 2},
            {'name': 'Eğitim', 'slug': 'egitim', 'order': 3},
            {'name': 'Arapça Eserler', 'slug': 'arapca-eserler', 'order': 4},
            {'name': 'Dini Kitaplar', 'slug': 'dini-kitaplar', 'order': 5},
            {'name': 'Kur\'an-ı Kerim', 'slug': 'kuran-i-kerim', 'order': 6},
            {'name': 'Çocuk Kitapları', 'slug': 'cocuk-kitaplari', 'order': 7},
            {'name': 'Çizgi Roman', 'slug': 'cizgi-roman', 'order': 8},
            {'name': 'Diğer Kitaplar', 'slug': 'diger-kitaplar', 'order': 9},
            {'name': 'Kaynak Kitaplar', 'slug': 'kaynak-kitaplar', 'order': 10},
            {'name': 'Tercüme Eserler', 'slug': 'tercume-eserler', 'order': 11},
        ],
        'Dergi': [
            {'name': 'Yedikıta Dergisi', 'slug': 'yedikita-dergisi', 'order': 1},
            {'name': 'İnsan ve Hayat Dergisi', 'slug': 'insan-ve-hayat-dergisi', 'order': 2},
            {'name': 'Çamlıca Çocuk Dergisi', 'slug': 'camlica-cocuk-dergisi', 'order': 3},
            {'name': 'Rüzgargülü Dergisi', 'slug': 'ruzgargulu-dergisi', 'order': 4},
            {'name': 'Çamlıca Kids Magazine', 'slug': 'camlica-cocuk-kids', 'order': 5},
            {'name': 'Rehber Zeka Dergisi', 'slug': 'rehber-zeka-dergisi', 'order': 6},
        ],
        'Takvim': [
            {'name': '2025 Takvim', 'slug': '2025-takvim', 'order': 1},
            {'name': 'Mobil Takvim', 'slug': 'mobil-takvim', 'order': 2},
        ],
        'Çocuklara Özel': [
            {'name': 'Okul Öncesi', 'slug': 'okul-oncesi', 'order': 1},
            {'name': 'İlkokul', 'slug': 'ilkogretim', 'order': 2},
            {'name': 'Ortaokul', 'slug': 'ortaogretim', 'order': 3},
        ],
        'Zeka Oyunları': [
            {'name': 'Faaliyet Kitapları', 'slug': 'faaliyet-kitaplari', 'order': 1},
            {'name': 'Puzzle', 'slug': 'puzzle', 'order': 2},
            {'name': 'Ahşap', 'slug': 'ahsap', 'order': 3},
            {'name': 'Kağıt', 'slug': 'kagit', 'order': 4},
            {'name': 'Plastik', 'slug': 'plastik', 'order': 5},
        ],
        'Dini Malzemeler': [
            {'name': 'Takke', 'slug': 'takke', 'order': 1},
            {'name': 'Tesbih', 'slug': 'tesbih', 'order': 2},
            {'name': 'Hac ve Umre Malzemeleri', 'slug': 'hac-ve-umre-malzemeleri', 'order': 3},
            {'name': 'Diğer Malzemeler', 'slug': 'diger-malzemeler', 'order': 4},
        ],
        'Kırtasiye': [
            {'name': '2024 Sanal Fuar Hediyeler', 'slug': '2024-sanal-fuar-hediyeler', 'order': 1},
            {'name': 'Okul Kırtasiye', 'slug': 'okul-kirtasiye', 'order': 2},
            {'name': 'Ofis Kırtasiye', 'slug': 'ofis-kirtasiye', 'order': 3},
            {'name': 'Hobi ve Sanat', 'slug': 'hobi-ve-sanat', 'order': 4},
            {'name': 'Kişisel Ürünler', 'slug': 'kisisel-urunler', 'order': 5},
        ],
    }
    
    # 3-cü mərhələ - Alt-alt kateqoriyalar
    sub_sub_categories = {
        'Tarih': [
            {'name': 'Kaynak Eserler', 'slug': 'kaynak-eserler', 'order': 1},
            {'name': 'Araştırma - İnceleme', 'slug': 'arastirma-inceleme', 'order': 2},
            {'name': 'Osmanlı Tarihi', 'slug': 'osmanli-tarihi', 'order': 3},
        ],
        'Edebiyat': [
            {'name': 'Hikâye', 'slug': 'hikaye', 'order': 1},
            {'name': 'Deneme', 'slug': 'deneme', 'order': 2},
            {'name': 'Biyografi', 'slug': 'biyografi', 'order': 3},
        ],
        'Eğitim': [
            {'name': 'Kişisel Gelişim', 'slug': 'kisisel-gelisim', 'order': 1},
            {'name': 'Çocuk Eğitimi Ve Gelişimi', 'slug': 'cocuk-egitimi-ve-gelisimi', 'order': 2},
            {'name': 'Dil Eğitimi', 'slug': 'dil-egitimi', 'order': 3},
        ],
        'Arapça Eserler': [
            {'name': 'Belagat-Edebiyat', 'slug': 'belagat-edebiyat', 'order': 1},
            {'name': 'Ders Kitapları', 'slug': 'ders-kitaplari', 'order': 2},
            {'name': 'Fıkıh ve Usûl-i Fıkıh', 'slug': 'fikih-usul-i-fikih', 'order': 3},
        ],
        'Dini Kitaplar': [
            {'name': 'Biyografi', 'slug': 'biyografi-dini', 'order': 1},
            {'name': 'İtikadi Mevzular', 'slug': 'itikadi-mevzular', 'order': 2},
            {'name': 'Dua Kitapları', 'slug': 'dua-kitaplari', 'order': 3},
        ],
        'Çocuk Kitapları': [
            {'name': 'Okul Öncesi', 'slug': 'okul-oncesi-kitap', 'order': 1},
            {'name': 'İlkokul', 'slug': 'ilkogretim-kitap', 'order': 2},
            {'name': 'Ortaokul', 'slug': 'ortaogretim-kitap', 'order': 3},
        ],
        'Çizgi Roman': [
            {'name': 'Osmanlı Denizcileri', 'slug': 'osmanli-denizcileri', 'order': 1},
            {'name': 'Osmanlı Sultanları', 'slug': 'osmanli-sultanlari', 'order': 2},
        ],
        'Diğer Kitaplar': [
            {'name': 'Diğer', 'slug': 'diger', 'order': 1},
            {'name': 'Gezi-Rehber', 'slug': 'gezi-rehber', 'order': 2},
            {'name': 'Kültür ve Sanat', 'slug': 'kultur-ve-sanat', 'order': 3},
        ],
        'Kaynak Kitaplar': [
            {'name': 'Sınav Kitapları', 'slug': 'sinav-kitaplari', 'order': 1},
            {'name': 'Açıköğretim Lise', 'slug': 'acikogretim-lise', 'order': 2},
        ],
        'Tercüme Eserler': [
            {'name': 'İngilizce Eserler', 'slug': 'ingilizce-eserler', 'order': 1},
            {'name': 'Almanca Eserler', 'slug': 'almanca-eserler', 'order': 2},
            {'name': 'Fransızca Eserler', 'slug': 'fransizca-eserler', 'order': 3},
        ],
        'Okul Kırtasiye': [
            {'name': 'Çanta Grubu', 'slug': 'canta-grubu', 'order': 1},
            {'name': 'Boya Grubu', 'slug': 'boya-grubu', 'order': 2},
            {'name': 'Kalem ve Yazı Gereçleri', 'slug': 'kalem-ve-yazi-gerecleri', 'order': 3},
        ],
        'Ofis Kırtasiye': [
            {'name': 'Kağıt Grubu', 'slug': 'kagit-grubu', 'order': 1},
            {'name': 'Dosyalama ve Arşivleme', 'slug': 'dosyalama-ve-arsivleme', 'order': 2},
            {'name': 'Diğer Ofis Gereçleri', 'slug': 'diger-ofis-gerecleri', 'order': 3},
        ],
        'Hobi ve Sanat': [
            {'name': 'Silikon Tabancası', 'slug': 'silikon-tabancasi', 'order': 1},
            {'name': 'Misina', 'slug': 'misina', 'order': 2},
            {'name': 'Kil', 'slug': 'kil', 'order': 3},
        ],
        'Kişisel Ürünler': [
            {'name': 'Hediyelik Eşyalar', 'slug': 'hediyelik-esyalar', 'order': 1},
            {'name': 'Aksesuarlar', 'slug': 'aksesuarlar', 'order': 2},
        ],
    }
    
    # Mövcud kateqoriyaları sil
    print("Mövcud kateqoriyalar silinir...")
    Category.objects.all().delete()
    
    # 1-ci mərhələ kateqoriyaları yarat
    print("1-ci mərhələ kateqoriyalar yaradılır...")
    main_cat_objects = {}
    for cat_data in main_categories:
        cat = Category.objects.create(
            name=cat_data['name'],
            slug=cat_data['slug'],
            level=1,
            order=cat_data['order'],
            is_leaf=False
        )
        main_cat_objects[cat_data['name']] = cat
        print(f"  ✓ {cat.name} (Level 1)")
    
    # 2-ci mərhələ kateqoriyaları yarat
    print("2-ci mərhələ kateqoriyalar yaradılır...")
    sub_cat_objects = {}
    for parent_name, sub_cats in sub_categories.items():
        parent = main_cat_objects[parent_name]
        for sub_cat_data in sub_cats:
            sub_cat = Category.objects.create(
                name=sub_cat_data['name'],
                slug=sub_cat_data['slug'],
                parent=parent,
                level=2,
                order=sub_cat_data['order'],
                is_leaf=True  # Əvvəlcə True, sonra alt kateqoriya varsa False olacaq
            )
            sub_cat_objects[sub_cat_data['name']] = sub_cat
            print(f"  ✓ {parent.name} → {sub_cat.name} (Level 2)")
    
    # 3-cü mərhələ kateqoriyaları yarat
    print("3-cü mərhələ kateqoriyalar yaradılır...")
    for parent_name, sub_sub_cats in sub_sub_categories.items():
        if parent_name in sub_cat_objects:
            parent = sub_cat_objects[parent_name]
            parent.is_leaf = False  # Alt kateqoriya var, is_leaf = False
            parent.save()
            
            for sub_sub_cat_data in sub_sub_cats:
                sub_sub_cat = Category.objects.create(
                    name=sub_sub_cat_data['name'],
                    slug=sub_sub_cat_data['slug'],
                    parent=parent,
                    level=3,
                    order=sub_sub_cat_data['order'],
                    is_leaf=True
                )
                print(f"  ✓ {parent.parent.name} → {parent.name} → {sub_sub_cat.name} (Level 3)")
    
    print(f"\n✅ 3 mərhələli kateqoriya strukturu yaradıldı!")
    print(f"📊 Cəmi {Category.objects.count()} kateqoriya yaradıldı")
    print(f"📊 1-ci mərhələ: {Category.objects.filter(level=1).count()}")
    print(f"📊 2-ci mərhələ: {Category.objects.filter(level=2).count()}")
    print(f"📊 3-cü mərhələ: {Category.objects.filter(level=3).count()}")

if __name__ == "__main__":
    create_hierarchical_categories()