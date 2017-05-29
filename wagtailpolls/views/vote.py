from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from wagtailpolls.forms import VoteForm
from wagtailpolls.models import Poll, Vote


def vote_data(poll):
    questions = poll.questions.all()
    votes = Vote.objects.filter(question__poll=poll)
    _vote_data = {
        'poll': poll.title,
        'total_questions': questions.count(),
        'total_votes': votes.count(),
        'votes': {
            question.question: question.votes.count()
            for question in questions
        }
    }
    return _vote_data


def _vote(request, poll_pk):
    """
    Performs the vote

    :param request: http request
    :param poll_pk: poll identifier
    :returns: JSON response
    """
    try:
        int(poll_pk)
    except ValueError:
        raise Http404("<h1>{0}</h1>".format('Oops, there is no poll to vote on!'))

    poll = get_object_or_404(Poll, pk=poll_pk)

    form = VoteForm(data=request.POST, poll=poll, request=request)

    if 'polls' in request.session:
        if poll.pk in request.session['polls']:
            return JsonResponse(vote_data(poll))
    else:
        request.session['polls'] = []

    if form.is_valid():
        form.save()
        request.session['polls'].append(poll.pk)
        request.session.modified = True
        return JsonResponse(vote_data(poll))

    else:
        data = vote_data(poll)
        data.update({'form_error': form.errors})
        return JsonResponse(data)


if getattr(settings, 'WAGTAILPOLLS_VOTE_REQUIRE_PERMS', None):
    vote = permission_required(settings.POLLS_VOTE_REQUIRE_PERMS)(_vote)
else:
    vote = _vote
