# Generated by Django 5.0.2 on 2024-02-28 12:13

import django.db.models.deletion
import document.models
import mptt.fields
import netbelge.path
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Başlık')),
                ('date', models.DateField(verbose_name='Tarih')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='Saat')),
                ('document_no', models.CharField(max_length=100, validators=[netbelge.path.validate_path], verbose_name='Belge/Dosya No')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_documents', to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan')),
                ('department', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='account.department', verbose_name='Birim')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_documents', to=settings.AUTH_USER_MODEL, verbose_name='Güncelleyen')),
            ],
            options={
                'verbose_name': 'Belge',
                'verbose_name_plural': 'Belgeler',
            },
        ),
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=1000, upload_to=document.models.upload_to, verbose_name='Dosya')),
                ('content', models.TextField(blank=True, null=True, verbose_name='İçerik')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_files', to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='document.document', verbose_name='Belge')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_files', to=settings.AUTH_USER_MODEL, verbose_name='Güncelleyen')),
            ],
            options={
                'verbose_name': 'Belge Dosyası',
                'verbose_name_plural': 'Belge Dosyaları',
            },
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Belge Türü')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('path', models.CharField(help_text='Dosyanın kaydedileceği klasörün dosya yolu.<br>Dosya yolu en fazla 63 karakter olmalıdır. <br>Dosya yolu en az 3 karakter olmalıdır. <br>Dosya yolu - veya / ile başlayamaz. <br>Dosya yolu - veya / ile bitemez. <br>Dosya yolu sadece harf, rakam, - ve / içerebilir.<br>{yil} {ay} {gun} {saat} {dakika} {saniye} {belge_no} değişkenlerini kullanabilirsiniz.', max_length=63, validators=[netbelge.path.validate_path], verbose_name='Dosya Yolu')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_document_types', to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan')),
                ('department', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_types', to='account.department', verbose_name='Birim')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_document_types', to=settings.AUTH_USER_MODEL, verbose_name='Güncelleyen')),
            ],
            options={
                'verbose_name': 'Belge Türü',
                'verbose_name_plural': 'Belge Türleri',
                'unique_together': {('department', 'name')},
            },
        ),
        migrations.AddField(
            model_name='document',
            name='document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='document.documenttype', verbose_name='Belge Türü'),
        ),
        migrations.CreateModel(
            name='DocumentSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Bölüm')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_sections', to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_sections', to=settings.AUTH_USER_MODEL, verbose_name='Güncelleyen')),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='document.documenttype', verbose_name='Belge Türü')),
            ],
            options={
                'verbose_name': 'Bölüm',
                'verbose_name_plural': 'Bölümler',
                'unique_together': {('document_type', 'name')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together={('department', 'document_type', 'document_no')},
        ),
    ]
