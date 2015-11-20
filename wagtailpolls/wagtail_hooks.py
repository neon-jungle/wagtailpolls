from __future__ import unicode_literals, absolute_import

from django.conf.urls import include, url
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from . import urls
from wagtail.wagtailadmin.menu import MenuItem


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^polls/', include(urls)),
    ]


@hooks.register('construct_main_menu')
def construct_main_menu(request, menu_items):
    menu_items.append(
        MenuItem(_('Polls'), urlresolvers.reverse('wagtailpolls_index'),
                 classnames='icon icon-group', order=250)
    )
