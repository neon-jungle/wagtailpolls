from __future__ import unicode_literals, absolute_import

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from ..forms import SearchForm
from ..pagination import paginate
from ..models import Poll


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def index(request):
    poll_list = Poll.objects.all()
    search_form = SearchForm()

    paginator, page = paginate(
        request,
        Poll.objects.all(),
        per_page=8)

    return render(request, 'wagtailpolls/index.html', {
        'page': page,
        'paginator': paginator,
        'poll_list': poll_list,
        'search_form': search_form,
    })


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def search(request, pk):
    poll_list = Poll.objects.all().order_by('-issue_date')
    search_form = SearchForm(request.GET or None)

    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        poll_list = poll_list.search(query)

    else:
        paginator, page = paginate(
            request,
            Poll.objects.order_by('-issue_date'),
            per_page=8)

    paginator, page = paginate(
        request,
        poll_list,
        per_page=20)

    return render(request, 'wagtailpolls/search.html', {
        'page': page,
        'paginator': paginator,
        'poll_list': poll_list,
        'search_form': search_form,
    })
