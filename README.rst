===============
wagtailpolls
===============

A plugin for Wagtail that provides polling functionality
`Documentation on ReadTheDocs <https://wagtailpolls.readthedocs.org/en/latest/>`_

Installing
==========

Install using pip::

    pip install wagtailpolls

It works with Wagtail 1.0b2 and upwards.

Using
=====

Add ``wagtailpolls`` to your ``INSTALLED_APPS``, add the line ``from wagtailpolls.views import vote`` to your ``urls.py`` and include the URL ``url(r'^vote/(?P<poll_pk>.*)/$', vote.vote, name='wagtailpolls_vote')``.

Define a foreign key referring to ``wagtailpolls.Poll`` and use the ``PollChooserPanel``:

.. code-block:: python

    from django.db import models
    from wagtailpolls.edit_handlers import PollChooserPanel
    from wagtail.wagtailadmin.edit_handlers import FieldPanel

    class Content(Page):
        body = models.TextField()
        poll = models.ForeignKey(
            'wagtailpolls.Poll',
            null=True,
            blank=True,
            on_delete=models.SET_NULL
        )

        content_panels = [
            FieldPanel('body', classname="full"),
            PollChooserPanel('poll'),
        ]


Settings
========

The following settings need to be set in your ``settings.py`` file.
``VOTE_COOLDOWN`` `This to be an integer representing minutes`
