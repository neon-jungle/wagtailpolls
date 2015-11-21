from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from .views import chooser, editor, results


urlpatterns = [
    # Choosers
    url(r'^choose/$', chooser.choose,
        name='wagtailpolls_choose'),
    url(r'^choose/(\w+)/(\w+)/$', chooser.choose, name='wagtailpolls_choose_specific'),
    url(r'^choose/(\d+)/$', chooser.chosen, name='wagtailpolls_chosen'),
    # General Urls
    url(r'^$', chooser.index,
        name='wagtailpolls_index'),
    url(r'^search/$', chooser.search,
        name='wagtailpolls_search'),
    url(r'^create/$', editor.create,
        name='wagtailpolls_create'),
    url(r'^edit/(?P<poll_pk>.*)/$', editor.edit,
        name='wagtailpolls_edit'),
    url(r'^delete/(?P<poll_pk>.*)/$', editor.delete,
        name='wagtailpolls_delete'),
    url(r'^copy/(?P<poll_pk>.*)/$', editor.copy,
        name='wagtailpolls_copy'),
    url(r'^results/(?P<poll_pk>.*)/$', results.results,
        name='wagtailpolls_results'),
]
