from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import BooleanField
from django.utils import timezone
default = timezone.now
class ProgramlamaDilleri(models.Model):
    isim = models.CharField(max_length=50)
    aktifMi = BooleanField(default=True)
    seoTitle = models.CharField(max_length=155)
    seoDescription = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Programlama Dili'
        verbose_name_plural = 'Programlama Dilleri'

    def __str__(self):
        return self.isim

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.isim)
        super(ProgramlamaDilleri, self).save(*args, **kwargs)
        return self.slug

class Kodlar(models.Model):
    kodTitle = models.CharField(max_length=100)
    kodDescription = models.TextField()
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    programlamaDili = models.ForeignKey('ProgramlamaDilleri', on_delete=models.CASCADE)
    aktifMi = BooleanField(default=True)
    seoTitle = models.CharField(max_length=155)
    seoDescription = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    resim = models.ImageField(upload_to='kodresimleri')
    tarih = models.TimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Kod'
        verbose_name_plural = 'Kodlar'

    def __str__(self):
        return self.kodTitle

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.kodTitle)
        super(Kodlar, self).save(*args, **kwargs)
        return self.slug

class Profil(models.Model):
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    motto = models.CharField(max_length=255, default="Henüz bir motto eklenmedi.")
    paylasim_sayisi = models.IntegerField(default=0)
    profil_fotografi = models.ImageField(upload_to='profil-resimleri', default='default.png')
    

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profiller"

    def __str__(self):
        return str(self.kullanici)