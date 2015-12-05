from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def querystring(context, **kwargs):
    get = context['request'].GET.copy()
    for key, val in kwargs.items():
        if val is None:
            get.pop(key, None)
        else:
            get[key] = val

    return get.urlencode()


@register.simple_tag(takes_context=True)
def vote(context, poll):
    if poll is None:
        return reverse('wagtailpolls_vote', kwargs={'poll_pk': None})
    return reverse('wagtailpolls_vote', kwargs={'poll_pk': poll.pk})
