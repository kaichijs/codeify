from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from kodlar.views import anasayfa, kod, kodlar, python, java, cplusplus, csharp, giris, login_request, logout_request, kayit, register, profil, profil_fotografi_guncelle, profil_duzenle, kod_paylas, kod_paylas_success, kod_onay, kod_incele_detay, kodonayla, kod_reddet, motto_guncelle

urlpatterns = [
    path('', anasayfa, name='anasayfa'),
    path('kodlar/', kodlar, name='kodlar'),
    path("admin/", admin.site.urls),
    path("python/", python, name='python'),
    path('java/', java, name='java'),
    path('cplusplus/', cplusplus, name='cplusplus'),  # Sonuna / eklendi
    path('csharp/', csharp, name='csharp'),
    path('giris/', giris, name='giris'),
    path('profil/<str:user>/', profil, name='profil'),
    path('kayit/', kayit, name='kayit'),
    path('login/', login_request, name='login_request'),
    path('logout/', logout_request, name='logout_request'),
    path('register/', register, name="register"),
    path('profil-duzenle/', profil_duzenle, name="profil_duzenle"),
    path('foto-guncelle/', profil_fotografi_guncelle, name='profil_fotografi_guncelle'),
    path('<str:programlamaDil>/<str:slug>/', kod, name='kod'),
    path('paylas/', kod_paylas, name='kod_paylas'),
    path('kod-paylas/success/', kod_paylas_success, name='kod_paylas_success'),
    path('kod-onayla/', kod_onay, name='kod_onay'),
    path('kod-incele-detay/<str:slug>', kod_incele_detay, name='kod_incele_detay'),
    path('kod-onayla/<str:slug>', kodonayla, name='kod_onayla'),
    path('kod-reddet/<str:slug>', kod_reddet, name='kod_reddet'),
    path('motto-guncelle', motto_guncelle, name='motto_guncelle'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)