from django.conf import settings
from django.core.paginator import Paginator, EmptyPage


def get_per_page():
    if hasattr(settings, 'DEFAULT_PER_PAGE'):
        per_page = settings.DEFAULT_PER_PAGE
    else:
        per_page = 12
    return per_page


def paginate(request, items, per_page=get_per_page(),
             page_key='page'):
    paginator = Paginator(items, per_page)

    try:
        page_number = int(request.GET[page_key])
        page = paginator.page(page_number)
    except (ValueError, KeyError, EmptyPage):
        page = paginator.page(1)

    return paginator, page
