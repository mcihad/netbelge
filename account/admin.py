from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _
from mptt.admin import TreeRelatedFieldListFilter

from document.models import DocumentType
from netbelge.path import normalize_path

from .models import Department


class DepartmentFilter(TreeRelatedFieldListFilter):
    title = "Üst Birim"
    parameter_name = "parent__id"


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "path", "created_at")
    search_fields = ("name", "description")
    list_filter = (("parent", DepartmentFilter),)
    ordering = ("path",)
    list_select_related = ("parent",)

    fieldsets = (
        (
            _("Birim Bilgileri"),
            {"fields": ("parent", "name", "path", "full_path")},
        ),
        (
            _("Açıklama"),
            {"fields": ("description",)},
        ),
        (
            _("Güncelleme Bilgileri"),
            {
                "fields": ("created_at", "updated_at", "created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = (
        "path",
        "full_path",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    def save_model(self, request, obj, form, change):
        obj.path = normalize_path(obj.name)
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description=_("Tam Dizin"))
    def full_path(self, obj):
        return obj.full_path
