import datetime

from django import forms
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy as __
from ipware.ip import get_ip, get_real_ip

from .models import Vote


# stop votes from an ip for 1 min after each vote


class SearchForm(forms.Form):
    query = forms.CharField(required=False)


class VoteForm(forms.ModelForm):
    question = forms.ModelChoiceField(Vote.objects.none(), widget=forms.RadioSelect, empty_label=None)

    class Meta:
        model = Vote
        fields = ['question']

    def __init__(self, poll, request=None, data=None, **kwargs):
        super(VoteForm, self).__init__(data, **kwargs)
        self.poll = poll
        self.request = request
        self.fields['question'].queryset = poll.questions.all()
        if request:
            self.ip = get_real_ip(self.request) or get_ip(self.request)

    def recent_vote(self):
        vote = Vote.objects.filter(ip=self.ip).order_by('-time')
        return vote.first()

    def clean(self):
        recent_vote = self.recent_vote()
        cooldown = getattr(settings, 'WAGTAILPOLLS_VOTE_COOLDOWN', 10)
        if not self.ip:
            self.add_error(None, _('Sorry, we were not able to obtain your ip address'))
        if recent_vote is not None:
            if timezone.now() - recent_vote.time < datetime.timedelta(minutes=cooldown):
                error_string = __(
                    'Sorry, you can not vote twice in a minute',
                    'Sorry, you can not vote twice in %(cooldown)s minutes',
                    cooldown) % {
                    'cooldown': cooldown
                }
                self.add_error(None, error_string)

    def save(self, commit=True):
        instance = super(VoteForm, self).save(commit=False)
        instance.ip = self.ip  # TODO
        if commit:
            instance.save()
        return instance
