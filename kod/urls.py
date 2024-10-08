from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from kodlar.views import anasayfa, kod, kodlar, python, java, cplusplus, csharp, giris, login_request, logout_request, kayit, register, profil, profil_fotografi_guncelle, profil_duzenle

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
    path('<str:programlamaDil>/<slug:slug>/', kod, name='kod'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)