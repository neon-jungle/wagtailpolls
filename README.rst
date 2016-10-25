===============
wagtailpolls
===============

A plugin for Wagtail that provides polling functionality.

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


Then, in your editor, ensure that you have added some polls in the polls section in wagtail admin. You will be able to select a poll from there accessable in the template as you would expect.

Templating & Display
====================
There are many ways in which you may want to display your poll. ``wagtailpolls`` comes with a template tag to assist with this, as well as certain attributes accessible via templating to render each question as a form. Here is an example using all of the tools provided:

.. code-block:: html

    {% extends "layouts/page.html" %}
    {% load wagtailpolls_tags %}
    {% block content %}
    <h1>{{ self.title }}</h1>
    <br>
    {% if self.poll %}
    <form class='poll' method='POST' action='{% vote self.poll %}'>
    {% csrf_token %}
    {{self.poll.form}}
    <br><br>
        <input type="submit" value="Vote">
    </form>
    {% else %}
        No polls added to this page yet!
    {% endif %}
    {% endblock %}

As shown, the ``{% vote %}`` template tag will need to be passed a poll instance to function correctly. You will also need to ``{% load wagtailpolls_tags %}`` at the top of the file where this template tag is used.
The poll can be rendered with all questions using ``.form`` at the end. ``.form_as_ul`` and all other form types will also work.

If you do select a poll for a page, no fields will display on the form and, upon voting, a message stating that there is no poll to vote on will be displayed.

Voting
======
When a vote has been submitted, the server will return a ``JsonResponse`` something like:

.. code-block:: json

    {"total_votes": 11, "total_questions": 3, "poll": "Test Poll", "votes": {"Nah": 10, "Yeah": 1, "Maybe": 0}}

With javascript, this data can be used to create a frontend for your poll to your own liking.

The voting form also performs some validation. If the voting form is unable to obtain your IP it will return something like:

.. code-block:: json

    {"poll": "Test Poll", "total_questions": 3, "total_votes": 11, "votes": {"Yeah": 1, "Maybe": 0, "Nah": 10}, "form_error": {"__all__": ["Sorry, we were not able to obtain your ip address"]}}

There is also a ``WAGTAILPOLLS_VOTE_COOLDOWN`` which is set in your settings. This will only allow users on the same IP to vote at an interval of your choosing. If this is caught, the error will be present in the ``JsonResponse`` much like the error above.

Additionally, information will be added to the django session (basically cookies will be set) that will help make sure devices are not able to vote twice. When a vote is rejected due to this reason, the vote simply won't register with no error being returned in the ``JsonResponse``.

Settings
========

The following settings can to be set in your ``settings.py`` file.

``WAGTAILPOLLS_VOTE_COOLDOWN`` `This is to be an integer representing minutes, the default is 10 minutes.`

``WAGTAILPOLLS_VOTE_REQUIRE_PERMS`` `A string or list of strings representing the permissions to vote, aka. 'wagtailadmin.access_admin'`
