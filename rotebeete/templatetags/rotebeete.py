from django import template
from juntagrico.entity.subs import Subscription

register = template.Library()


@register.filter
def subscription_overview(subscription: Subscription):
    result = ['<ul>']
    for part in subscription.active_parts:
        result.append(f"<li>{part.type.name} {part.type.size.units}x{part.type.size.product}</li>")
    result.append('</ul>')
    return '\n'.join(result)
