# Generated by Django 5.1.1 on 2024-10-04 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kodlar", "0002_remove_programdillerikategori_ustkategori"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ProgramDilleriKategori",
            new_name="ProgramlamaDilleri",
        ),
    ]
