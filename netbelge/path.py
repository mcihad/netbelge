import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def normalize_path(name: str) -> str:
    tr_map = name.maketrans("ğĞıİöÖüÜşŞçÇ", "ggiioouusscc")
    path = name.translate(tr_map)
    path = path.lower().replace(" ", "-")
    parts = path.split("-")
    path = "-".join([part.replace("-", "") for part in parts if part])
    if path.startswith("/") or path.startswith("-"):
        path = path[1:]
    if path.endswith("/") or path.endswith("-"):
        path = path[:-1]

    if len(path) > 63:
        path = path[:63]
    if len(path) < 3:
        if len(path) == 0:
            path = "birim"
        else:
            path = path + "-birim"
    return path


def validate_path(value):
    # Rules for path:
    # - Must be unique
    # - Must be at most 63 characters
    # - Must be at least 3 characters
    # - Must not contain special characters only letters, numbers and hyphen and /
    # - Must not start with hyphen or /
    # - Must not end with hyphen or /
    # - Must have placeholder value {yil} {ay} {gun} {saat} {dakika} {saniye} {belge_turu} {belge_no}
    # - Must not contain Turkish characters
    allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789/-"
    # replace {yil} {ay} {gun} {saat} {dakika} {saniye} {belge_turu} {belge_no}
    placeholders = [
        "{yil}",
        "{ay}",
        "{gun}",
        "{saat}",
        "{dakika}",
        "{saniye}",
        "{belge_turu}",
        "{belge_no}",
    ]

    placeholders_default = {
        "{yil}": "yil",
        "{ay}": "ay",
        "{gun}": "gun",
        "{saat}": "saat",
        "{dakika}": "dakika",
        "{saniye}": "saniye",
        "{belge_turu}": "belge-turu",
        "{belge_no}": "belge-no",
    }
    # find all placeholders
    found_placeholders = re.findall(r"{\w+}", value)
    # check if all placeholders are valid
    for placeholder in found_placeholders:
        if placeholder not in placeholders:
            raise ValidationError(
                _("Geçersiz değişken: {placeholder}").format(placeholder=placeholder)
            )

    value = value.replace("{yil}", "yil")
    value = value.replace("{ay}", "ay")
    value = value.replace("{gun}", "gun")
    value = value.replace("{saat}", "saat")
    value = value.replace("{dakika}", "dakika")
    value = value.replace("{saniye}", "saniye")
    value = value.replace("{belge_turu}", "belge-turu")
    value = value.replace("{belge_no}", "belge-no")

    if len(value) > 63:
        raise ValidationError(_("Dosya yolu en fazla 63 karakter olmalıdır."))
    if len(value) < 3:
        raise ValidationError(_("Dosya yolu en az 3 karakter olmalıdır."))

    if value[0] in "-/":
        raise ValidationError(_("Dosya yolu - veya / ile başlayamaz."))
    if value[-1] in "-/":
        raise ValidationError(_("Dosya yolu - veya / ile bitemez."))
    for char in value:
        if char not in allowed_chars:
            raise ValidationError(
                _("Dosya yolu sadece harf, rakam, - ve / içerebilir.")
            )
    return value
