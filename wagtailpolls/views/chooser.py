from __future__ import absolute_import, unicode_literals

import json

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render
from django.utils.six import text_type
from django.utils.translation import ugettext as _
from wagtail.wagtailadmin.forms import SearchForm as AdminSearchForm
from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
from wagtail.wagtailsearch.backends import get_search_backend

from ..forms import SearchForm
from ..models import Poll
from ..pagination import paginate


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
def search(request):
    poll_list = Poll.objects.all()
    search_form = SearchForm(request.GET or None)

    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        poll_list = poll_list.search(query)

    else:
        paginator, page = paginate(
            request,
            Poll.objects.all(),
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


def choose(request):
    items = Poll.objects.all()

    # Search
    is_searching = False
    search_query = None
    if 'q' in request.GET:
        search_form = AdminSearchForm(request.GET, placeholder=_("Search %(snippet_type_name)s") % {
            'snippet_type_name': 'Polls'
        })

        if search_form.is_valid():
            search_query = search_form.cleaned_data['q']

            search_backend = get_search_backend()
            items = search_backend.search(search_query, items)
            is_searching = True

    else:
        search_form = AdminSearchForm()

    # Pagination
    paginator, paginated_items = paginate(request, items, per_page=25)

    # If paginating or searching, render "results.html"
    if request.GET.get('results', None) == 'true':
        return render(request, "wagtailpolls/search_results.html", {
            'items': paginated_items,
            'query_string': search_query,
            'is_searching': is_searching,
        })

    return render_modal_workflow(
        request,
        'wagtailpolls/choose.html', 'wagtailpolls/choose.js',
        {
            'snippet_type_name': 'Poll',
            'items': paginated_items,
            'is_searchable': True,
            'search_form': search_form,
            'query_string': search_query,
            'is_searching': is_searching,
        }
    )


def chosen(request, id):
    model = Poll
    item = get_object_or_404(model, id=id)

    snippet_json = json.dumps({
        'id': item.id,
        'string': text_type(item),
    })

    return render_modal_workflow(
        request,
        None, 'wagtailpolls/chosen.js',
        {
            'snippet_json': snippet_json,
        }
    )
