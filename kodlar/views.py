from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.text import slugify

from .models import ProgramlamaDilleri, Kodlar, Profil, KodInceleme
from .forms import ProfilFotoForm, KodPaylasForm, ProfilForm
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

@login_required
def kod_paylas_success(request):
    success_message = "Kod başarıyla paylaşıldı!"
    form = KodPaylasForm()
    return render(request, 'paylas.html', {'form': form, 'success_message': success_message})

@login_required
def kod_paylas(request):
    form = KodPaylasForm()  # Formu başlatıyoruz
    success_message = None  # Başarı mesajını başlatıyoruz
    error_message = None  # Hata mesajını başlatıyoruz

    # Cooldown süresi (örneğin 10 dakika)
    cooldown_suresi = timedelta(minutes=2)

    profil = Profil.objects.get(kullanici=request.user)

    if not request.user.is_superuser:
        # Eğer son paylaşım zamanı varsa ve cooldown dolmadıysa hata mesajı döndür
        if profil.son_paylasim_zamani and timezone.now() - profil.son_paylasim_zamani < cooldown_suresi:
            kalan_sure = cooldown_suresi - (timezone.now() - profil.son_paylasim_zamani)
            if kalan_sure.seconds <= 60:
                error_message = f"Tekrar kod paylaşabilmek için {kalan_sure.seconds} saniye beklemelisiniz."
            else:
                error_message = f"Tekrar kod paylaşabilmek için {kalan_sure.seconds // 60} dakika beklemelisiniz."
            return render(request, 'paylas.html',
                          {'form': form, 'success_message': success_message, 'error_message': error_message})

    if request.method == 'POST':  # POST isteği geldiğinde
        form = KodPaylasForm(request.POST, request.FILES)
        try:
            if form.is_valid():  # Form geçerliyse
                kod = form.save(commit=False)  # Veritabanına kaydetmeden önce formu beklet
                kod.kullanici = request.user  # Oturum açmış kullanıcıyı atıyoruz
                kod.slug = slugify(kod.kodTitle)  # Slugify ile başlık kısmından slug oluşturuyoruz
                kod.save()  # Şimdi kaydediyoruz

                success_message = "Kod başarıyla paylaşıldı!"  # Başarı mesajı
                return redirect('kodlar')  # Paylaşılan kodlar sayfasına yönlendir
            else:
                error_message = "Formda geçersiz veriler var. Lütfen tekrar deneyin."
                print(form.errors)  # Formdaki hataları yazdır
        except Exception as e:
            error_message = f"Bir hata oluştu: {str(e)}"

    return render(request, 'paylas.html',
                  {'form': form, 'success_message': success_message, 'error_message': error_message})

def kod_onay(request):
    bekleyen_kodlar = KodInceleme.objects.all()
    return render(request, 'kod-onay.html', {'kod': bekleyen_kodlar})

def kod_incele_detay(request, slug):
    kod_inceleme = get_object_or_404(KodInceleme, slug=slug)
    return render(request, 'kod-incele-detay.html', {'kod_inceleme': kod_inceleme})

@login_required()
def kodonayla(request, slug):
    if not request.user.is_superuser:
        return redirect('anasayfa')  # Yetkisiz kullanıcıyı yönlendirin
    # KodInceleme modelinden pk'ya göre kayıt getir
    kod_inceleme = get_object_or_404(KodInceleme, slug=slug)
    profil = Profil.objects.get(kullanici=kod_inceleme.kullanici)
    # İlişkili programlama dilinin olup olmadığını kontrol edin
    if not kod_inceleme.programlamaDili:
        messages.error(request, "İlişkili programlama dili bulunamadı.")
        return redirect('anasayfa')  # Uygun bir hata sayfasına yönlendirin

    # Kodlar modeline yeni bir kayıt oluştur
    yeni_kod = Kodlar(
        kodTitle=kod_inceleme.kodTitle,
        kodDescription=kod_inceleme.kodDescription,
        kullanici=kod_inceleme.kullanici,
        seoDescription=kod_inceleme.seoDescription,
        programlamaDili=kod_inceleme.programlamaDili,  # ForeignKey alanı
        seoTitle=kod_inceleme.kodTitle,
        slug=kod_inceleme.slug,
        resim=kod_inceleme.resim,
        tarih=kod_inceleme.tarih,
    )
    # Profiline 1 paylasım ekleme
    profil.paylasim_sayisi += 1
    profil.son_paylasim_zamani = timezone.now()
    profil.save()

    # Yeni kaydı kaydet
    yeni_kod.save()

    # KodInceleme kaydını sil
    kod_inceleme.delete()

    # Başarılı işlemden sonra yönlendirme yap
    return redirect('kod_onay')

@login_required()
def kod_reddet(request, slug):
    if not request.user.is_superuser:
        return redirect('anasayfa')
    kod = get_object_or_404(KodInceleme, slug=slug)
    kod.delete()
    return redirect('kod_onay')


@login_required
def motto_guncelle(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        profil = Profil.objects.get(kullanici=request.user)

        # Formu mevcut verilerle dolduruyoruz
        form = ProfilForm(request.POST, instance=profil)

        if form.is_valid():
            form.save()  # Form verisi doğrulandıktan sonra kaydediliyor
            return JsonResponse({'status': 'success'})
        else:
            # Form hataları varsa hata mesajlarını döndür
            return JsonResponse({'status': 'fail', 'errors': form.errors}, status=400)

    return JsonResponse({'status': 'fail'}, status=400)