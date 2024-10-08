from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ProgramlamaDilleri, Kodlar, Profil
from .forms import ProfilFotoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from django.contrib import messages  # Hata mesajları için

def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('giris')

def login_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('kodlar')
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı!")
            return render(request, 'giris.html', {'error': 'Kullanıcı adı veya şifre hatalı!'})

    # GET isteği ile giriş sayfasını render et
    return render(request, 'giris.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('re-password')

        if password != repassword:
            messages.error(request, "Girilen şifreler uyuşmuyor!")
            return render(request, 'kayit.html', {'error': 'Girilen şifreler uyuşmuyor!'})
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış!")
            return render(request, 'kayit.html', {'error': 'Bu kullanıcı adı zaten alınmış!'})
        
        user = User.objects.create_user(username=username,password=password)
        user.save()
        user = authenticate(request, username=username, password=password)
        login(request, user)
        Profil.objects.create(kullanici=user,paylasim_sayisi=0)
        return redirect('anasayfa')
    return render(request, 'anasayfa.html')

def giris(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'giris.html')

def kayit(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'kayit.html')

def anasayfa(request):
    diller = ProgramlamaDilleri.objects.all()
    kod = Kodlar.objects.all()
    return render(request, 'index.html', {'diller': diller, 'kod': kod})

def kodlar(request):
    diller = ProgramlamaDilleri.objects.all()
    kod = Kodlar.objects.filter(aktifMi=True)
    return render(request, 'kodlar.html', {'kod': kod, 'diller': diller})

def kod(request, slug, programlamaDil):
    diller = get_object_or_404(ProgramlamaDilleri, slug=programlamaDil)
    kod = get_object_or_404(Kodlar, slug=slug)
    return render(request, 'kod.html', {'kod': kod, 'diller': diller})

def python(request):
    kodlar = Kodlar.objects.filter(aktifMi=True)
    diller = ProgramlamaDilleri.objects.all()
    return render(request, 'python.html', { 'kodlar': kodlar , 'diller': diller})

def java(request):
    kodlar = Kodlar.objects.filter(aktifMi=True)
    diller = ProgramlamaDilleri.objects.all()
    return render(request, 'java.html', { 'kodlar': kodlar, 'diller': diller})

def cplusplus(request):
    kodlar = Kodlar.objects.filter(aktifMi=True)
    diller = ProgramlamaDilleri.objects.all()
    return render(request, 'cplusplus.html', { 'kodlar': kodlar, 'diller': diller})

def csharp(request):
    kodlar = Kodlar.objects.filter(aktifMi=True)
    diller = ProgramlamaDilleri.objects.all()
    return render(request, 'csharp.html', { 'kodlar': kodlar, 'diller': diller})

def profil(request, user):
    kullanici = get_object_or_404(User, username=user)
    profil = get_object_or_404(Profil, kullanici=kullanici)

    return render(request, 'profil.html', {'profil': profil, 'kullanici': kullanici})

def profil_duzenle(request):
    profil = get_object_or_404(Profil, kullanici=request.user)
    return render(request, 'profil-duzenle.html', {'profil': profil})


from django.http import JsonResponse

@login_required
def profil_fotografi_guncelle(request):
    profil = Profil.objects.get(kullanici=request.user)

    if request.method == 'POST':
        form = ProfilFotoForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            # JSON yanıtı ile yeni profil fotoğrafının URL'sini döndür
            return JsonResponse({'new_photo_url': profil.profil_fotografi.url})
        else:
            return JsonResponse({'error': 'Form geçersiz'}, status=400)

    return JsonResponse({'error': 'Geçersiz istek'}, status=400)
