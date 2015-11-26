from __future__ import absolute_import, unicode_literals

from six import text_type

from django.db import models
from django.utils.text import slugify
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailsearch.backends import get_search_backend
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailsearch import index


class PollQuerySet(QuerySet):
    def search(self, query_string, fields=None, backend='default'):
        """
        This runs a search query on all the pages in the QuerySet
        """
        search_backend = get_search_backend(backend)
        return search_backend.search(query_string, self)


@python_2_unicode_compatible
class Vote(models.Model):
    question = ParentalKey('Question', related_name='votes')
    ip = models.GenericIPAddressField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question.question


@python_2_unicode_compatible
class Question(ClusterableModel, models.Model):
    poll = ParentalKey('Poll', related_name='questions')
    question = models.CharField(max_length=128)

    def __str__(self):
        return self.question


@python_2_unicode_compatible
class Poll(ClusterableModel, models.Model, index.Indexed):
    title = models.CharField(max_length=128)
    date_created = models.DateTimeField(default=timezone.now)

    panels = [
        FieldPanel('title'),
        InlinePanel('questions', label='Questions', min_num=1)
    ]

    search_fields = (
        index.SearchField('title', partial_match=True, boost=5),
        index.SearchField('id', boost=10),
    )

    objects = PollQuerySet.as_manager()

    def get_nice_url(self):
        return slugify(text_type(self))

    def get_template(self, request):
        try:
            return self.template
        except AttributeError:
            return '{0}/{1}.html'.format(self._meta.app_label, self._meta.model_name)

    def form(self):
        return VoteForm(self)

    def __str__(self):
        return self.title


# Stops circular import
from .forms import VoteForm
