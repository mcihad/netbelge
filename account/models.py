from django.contrib.auth.models import User
from django.db import models
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from netbelge.path import normalize_path


class Department(MPTTModel):
    name = models.CharField(_("Birim"), max_length=100)
    parent = TreeForeignKey(
        "self",
        verbose_name=_("Üst Birim"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
    )

    path = models.CharField(
        _("Dizin"),
        max_length=63,
        blank=True,
        editable=False,
        null=True,
    )

    description = models.TextField(_("Açıklama"), blank=True, null=True)

    created_at = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Güncellenme Tarihi"), auto_now=True)
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Oluşturan"),
        on_delete=models.CASCADE,
        related_name="created_departments",
    )

    updated_by = models.ForeignKey(
        User,
        verbose_name=_("Güncelleyen"),
        on_delete=models.CASCADE,
        related_name="updated_departments",
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Birim")
        verbose_name_plural = _("Birimler")
        unique_together = ("name", "parent")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.path = normalize_path(self.name)
        super().save(*args, **kwargs)

    @property
    def full_path(self):
        if self.parent:
            return f"{self.parent.full_path}/{self.path}"
        return self.path
