from django import template
from django.utils.translation import gettext as _
from juntagrico.entity.subs import Subscription

register = template.Library()


@register.filter
def subscription_overview(subscription: Subscription):
    result = ['<ul>']
    for part in subscription.active_parts:
        result.append(f"<li>{part.type.name} / {part.type.size.units}x{part.type.size.product} / {part.type.price} €</li>")
    result.append('</ul>')
    return '\n'.join(result)


@register.filter
def disable_iban(form):
    form.fields["iban"].disabled = True
    form.fields['iban'].help_text = form.contact_admin_link(_('Kontaktiere {} um die IBAN zu ändern.'))
    return form
