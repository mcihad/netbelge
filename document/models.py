from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import TreeForeignKey

from account.models import Department
from netbelge.path import normalize_path, validate_path


class DocumentType(models.Model):
    department = TreeForeignKey(
        Department,
        verbose_name=_("Birim"),
        on_delete=models.CASCADE,
        related_name="document_types",
    )
    name = models.CharField(_("Belge Türü"), max_length=50)
    description = models.TextField(_("Açıklama"), blank=True, null=True)
    path = models.CharField(
        _("Dosya Yolu"),
        max_length=63,
        validators=[validate_path],
        help_text=_(
            "Dosyanın kaydedileceği klasörün dosya yolu.<br>"
            "Dosya yolu en fazla 63 karakter olmalıdır. <br>"
            "Dosya yolu en az 3 karakter olmalıdır. <br>"
            "Dosya yolu - veya / ile başlayamaz. <br>"
            "Dosya yolu - veya / ile bitemez. <br>"
            "Dosya yolu sadece harf, rakam, - ve / içerebilir.<br>"
            "{yil} {ay} {gun} {saat} {dakika} {saniye} {belge_no} değişkenlerini kullanabilirsiniz."
        ),
    )

    created_at = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Güncellenme Tarihi"), auto_now=True)
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Oluşturan"),
        on_delete=models.CASCADE,
        related_name="created_document_types",
    )

    updated_by = models.ForeignKey(
        User,
        verbose_name=_("Güncelleyen"),
        on_delete=models.CASCADE,
        related_name="updated_document_types",
    )

    class Meta:
        verbose_name = _("Belge Türü")
        verbose_name_plural = _("Belge Türleri")
        unique_together = ("department", "name")

    def __str__(self):
        return self.name

    def full_path(self):
        return f"{self.department.full_path}/{self.path}"


class DocumentSection(models.Model):
    document_type = models.ForeignKey(
        DocumentType,
        verbose_name=_("Belge Türü"),
        on_delete=models.CASCADE,
        related_name="sections",
    )
    name = models.CharField(_("Bölüm"), max_length=100)
    description = models.TextField(_("Açıklama"), blank=True, null=True)

    created_at = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Güncellenme Tarihi"), auto_now=True)
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Oluşturan"),
        on_delete=models.CASCADE,
        related_name="created_sections",
    )

    updated_by = models.ForeignKey(
        User,
        verbose_name=_("Güncelleyen"),
        on_delete=models.CASCADE,
        related_name="updated_sections",
    )

    class Meta:
        verbose_name = _("Bölüm")
        verbose_name_plural = _("Bölümler")
        unique_together = ("document_type", "name")

    def __str__(self):
        return self.name


class Document(models.Model):
    department = TreeForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Birim"),
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Belge Türü"),
    )
    title = models.CharField(_("Başlık"), max_length=100)
    date = models.DateField(
        _("Tarih"),
    )

    time = models.TimeField(_("Saat"), blank=True, null=True)

    document_no = models.CharField(
        _("Belge/Dosya No"), max_length=100, validators=[validate_path]
    )
    description = models.TextField(_("Açıklama"), blank=True, null=True)

    created_at = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Güncellenme Tarihi"), auto_now=True)
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Oluşturan"),
        on_delete=models.CASCADE,
        related_name="created_documents",
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name=_("Güncelleyen"),
        on_delete=models.CASCADE,
        related_name="updated_documents",
    )

    class Meta:
        verbose_name = _("Belge")
        verbose_name_plural = _("Belgeler")
        unique_together = ("department", "document_type", "document_no")

    def __str__(self):
        return self.title


def upload_to(instance, filename):
    path = instance.document.document_type.full_path()
    path = path.replace("{yil}", str(instance.document.date.year))
    path = path.replace("{ay}", str(instance.document.date.month))
    path = path.replace("{gun}", str(instance.document.date.day))
    path = path.replace(
        "{belge_no}",
        normalize_path(instance.document.document_no),
    )
    return f"{path}/{filename}"


class DocumentFile(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name=_("Belge"),
    )
    file = models.FileField(
        _("Dosya"),
        upload_to=upload_to,
        max_length=1000,
    )
    content = models.TextField(_("İçerik"), blank=True, null=True)

    created_at = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Güncellenme Tarihi"), auto_now=True)
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Oluşturan"),
        on_delete=models.CASCADE,
        related_name="created_files",
    )

    updated_by = models.ForeignKey(
        User,
        verbose_name=_("Güncelleyen"),
        on_delete=models.CASCADE,
        related_name="updated_files",
    )

    class Meta:
        verbose_name = _("Belge Dosyası")
        verbose_name_plural = _("Belge Dosyaları")

    def __str__(self):
        return self.file.name
