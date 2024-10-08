from django.contrib import admin

from .models import ProgramlamaDilleri, Kodlar, Profil

class ProgramlamaDilleriAdmin(admin.ModelAdmin):
    list_display = ['isim', 'aktifMi', 'slug']
    list_filter = ['aktifMi']
    search_fields = ['isim', 'slug']

class KodlarAdmin(admin.ModelAdmin):
    list_display = ['kodTitle', 'slug', 'programlamaDili','aktifMi', 'tarih']
    list_filter = ['aktifMi', 'programlamaDili']
    search_fields = ['slug', 'kodTitle']

class ProfilAdmin(admin.ModelAdmin):
    list_display = ['kullanici', 'paylasim_sayisi', 'profil_fotografi', 'motto']
    list_filter = ['paylasim_sayisi']
    search_fields = ['kullanici']

admin.site.register(Profil, ProfilAdmin)
admin.site.register(ProgramlamaDilleri, ProgramlamaDilleriAdmin)
admin.site.register(Kodlar, KodlarAdmin)