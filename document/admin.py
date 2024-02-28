from django import forms
from django.contrib import admin
from django.db import models
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _

from account.admin import DepartmentFilter

from .models import Document, DocumentFile, DocumentSection, DocumentType


class SectionInline(admin.TabularInline):
    model = DocumentSection
    extra = 0

    formfield_overrides = {
        models.TextField: {"widget": forms.TextInput(attrs={"size": 50})},
    }
    readonly_fields = ("created_by", "updated_by")


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "path")
    search_fields = ("name", "description")
    list_filter = (("department", DepartmentFilter),)
    inlines = [SectionInline]

    fieldsets = (
        (
            _("Belge Türü Bilgileri"),
            {
                "fields": (
                    "department",
                    "name",
                    "path",
                    "full_path",
                )
            },
        ),
        (
            _("Açıklama"),
            {"fields": ("description",)},
        ),
        (
            _("Güncelleme Bilgileri"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "created_by",
                    "updated_by",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = (
        "full_path",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    def full_path(self, obj):
        return f"{obj.department.full_path}/{obj.path}"

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.updated_by = request.user
            if not change:
                instance.created_by = request.user
            instance.save()
        formset.save_m2m()


class DocumentFileInline(admin.StackedInline):
    model = DocumentFile
    extra = 0
    readonly_fields = ("file_link",)

    @admin.display(description=_("Dosya"))
    def file_link(self, obj):
        return format_html_join(
            "\n",
            '<a href="{}">{}</a>',
            ((file.file.url, file.file) for file in obj.files.all()),
        )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "document_type",
        "date",
        "document_no",
        "department",
    )

    list_filter = (
        "document_type",
        ("department", DepartmentFilter),
    )

    search_fields = ("title", "document_no", "description")
    date_hierarchy = "date"

    inlines = (DocumentFileInline,)
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (
            _("Belge Bilgileri"),
            {"fields": ("department", "document_type", "title", "date", "document_no")},
        ),
        (
            _("Açıklama"),
            {"fields": ("description",)},
        ),
        (
            _("Güncelleme Bilgileri"),
            {"fields": ("created_at", "updated_at", "created_by", "updated_by")},
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.updated_by = request.user
            if not change:
                instance.created_by = request.user
            instance.save()
        formset.save_m2m()


admin.site.site_header = _("NetBelge Yönetim Paneli")
admin.site.site_title = _("NetBelge Yönetim Paneli")
admin.site.index_title = _("NetBelge Yönetim Paneli")
