from crispy_forms import layout
from django import forms, template
from django.db.models import Sum
from django.utils.translation import gettext as _
from juntagrico.forms import MemberProfileForm

register = template.Library()


@register.filter
def disable_iban(form: MemberProfileForm):
    masked_iban = "".join(
        [
            c if i in [0, 1, 2, 3, 20, 21] else "*"
            for i, c in enumerate(form.initial["iban"])
        ]
    )
    form.fields["shadow_iban"] = forms.CharField(
        initial=masked_iban,
        disabled=True,
        label="IBAN",
        required=False,
        help_text=form.contact_admin_link(_("Kontaktiere {email} um die IBAN zu ändern.")),
    )
    form.helper.layout.fields.insert(
        form.helper.layout.fields.index("iban") + 1, "shadow_iban"
    )
    form.helper.layout.fields.remove("iban")
    form.helper.layout.fields.append(layout.Field("iban", type="hidden"))
    return form


@register.filter
def subtype_units(subtype):
    """Return aggregated units for v2 subtype bundles; 0 when unavailable."""
    try:
        return subtype.bundle.product_sizes.aggregate(units=Sum("units"))["units"] or 0
    except AttributeError:
        return 0
