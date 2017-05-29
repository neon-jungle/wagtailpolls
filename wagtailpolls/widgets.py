from __future__ import absolute_import, unicode_literals

import json
from django.contrib.contenttypes.models import ContentType

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.widgets import AdminChooser


class AdminPollChooser(AdminChooser):
    target_content_type = None

    class Media:
        js = ['js/poll_chooser.js']

    def __init__(self, content_type=None, **kwargs):
        model = kwargs.pop('model', None)
        self.choose_one_text = (_('Choose a poll'))
        self.choose_another_text = (_('Choose another poll'))
        self.link_to_chosen_text = (_('Edit this poll'))

        super(AdminPollChooser, self).__init__(**kwargs)
        if content_type is not None:
            self.target_content_type = content_type
        elif model is not None:
            self.target_content_type = ContentType.objects.get_for_model(model)
        else:
            raise RuntimeError("Unable to set model from both content_type and model")

    def render_html(self, name, value, attrs):
        model_class = self.target_content_type.model_class()
        instance, value = self.get_instance_and_id(model_class, value)

        original_field_html = super(AdminPollChooser, self).render_html(name, value, attrs)

        return render_to_string("widgets/poll_chooser.html", {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'item': instance,
        })

    def render_js_init(self, id_, name, value):
        return "createPollChooser({id});".format(id=json.dumps(id_))
