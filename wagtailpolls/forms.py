from django import forms
from .models import Vote
from ipware.ip import get_real_ip, get_ip
from django.conf import settings
from django.utils import timezone
import datetime

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
        if not self.ip:
            self.add_error(None, 'Sorry, we were not able to obtain your ip address')
        if recent_vote is not None:
            if timezone.now() - recent_vote.time < datetime.timedelta(minutes=settings.VOTE_COOLDOWN):
                self.add_error(None, 'Sorry, you cannot vote twice in %s minutes' % (settings.VOTE_COOLDOWN))

    def save(self, commit=True):
        instance = super(VoteForm, self).save(commit=False)
        instance.ip = self.ip  # TODO
        if commit:
            instance.save()
        return instance
