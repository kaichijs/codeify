# Generated by Django 5.1.1 on 2024-10-04 22:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kodlar", "0003_rename_programdillerikategori_programlamadilleri"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Kodlar",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("kodTitle", models.CharField(max_length=100)),
                ("kodDescription", models.TextField()),
                ("aktifMi", models.BooleanField(default=True)),
                ("seoTitle", models.CharField(max_length=155)),
                ("seoDescription", models.TextField(blank=True, null=True)),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                ("resim", models.ImageField(upload_to="kodresimleri")),
                ("tarih", models.TimeField(auto_now_add=True)),
                (
                    "kullanici",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Kod",
                "verbose_name_plural": "Kodlar",
            },
        ),
    ]
