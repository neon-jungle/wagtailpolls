from __future__ import absolute_import, unicode_literals

from six import text_type

from django.db import models
from django.shortcuts import render
from django.utils.text import slugify
from django.db.models.query import QuerySet
from django.utils import timezone
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch.backends import get_search_backend


class PollQuerySet(QuerySet):
    def search(self, query_string, fields=None, backend='default'):
        """
        This runs a search query on all the pages in the QuerySet
        """
        search_backend = get_search_backend(backend)
        return search_backend.search(query_string, self)


class Poll(models.Model):
    issue_date = models.DateTimeField('Issue date', default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('issue_date'),
    ]

    objects = PollQuerySet.as_manager()

    def get_nice_url(self):
        return slugify(text_type(self))

    def get_template(self, request):
        try:
            return self.template
        except AttributeError:
            return '{0}/{1}.html'.format(self._meta.app_label, self._meta.model_name)

    def serve(self, request):
        return render(request, self.get_template(request), {
            'poll': self,
        })

# Need to import this down here to prevent circular imports :(
from .views import frontend
