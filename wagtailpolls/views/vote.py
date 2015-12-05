from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from ..forms import VoteForm
from ..models import Poll, Vote


def vote_data(poll):
    questions = poll.questions.all()
    votes = Vote.objects.filter(question__poll=poll)
    vote_data = {
        'poll': poll.title,
        'total_questions': questions.count(),
        'total_votes': votes.count(),
        'votes': {
            question.question: question.votes.count()
            for question in questions
        }
    }
    return vote_data


@permission_required('wagtailadmin.access_admin')
def vote(request, poll_pk):
    try:
        int(poll_pk)

    except ValueError:
        return HttpResponse("<h1>Oops, there is no poll to vote on!</h1>", status=500)

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
        data.update({
            'form_error': form.errors
            })
        return JsonResponse(data)

    return HttpResponse("<h1> 403 Forbidden</h1>", status=403)
