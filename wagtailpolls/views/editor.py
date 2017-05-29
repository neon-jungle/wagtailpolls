from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.lru_cache import lru_cache

from wagtail.wagtailadmin.edit_handlers import (
    ObjectList, extract_panel_definitions_from_model_class)
from wagtail.wagtailcore.models import Page


@lru_cache(maxsize=None)
def get_poll_edit_handler(Poll):
    panels = extract_panel_definitions_from_model_class(Poll)
    EditHandler = ObjectList(panels).bind_to_model(Poll)
    return EditHandler


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def create(request):
    from ..models import Poll

    poll = Poll()
    EditHandler = get_poll_edit_handler(Poll)
    EditForm = EditHandler.get_form_class(Poll)

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=poll)
        if form.is_valid():
            poll = form.save()
            poll.save()
            messages.success(request, _('The poll "{0!s}" has been added').format(poll))
            return redirect('wagtailpolls_index')

        else:
            messages.error(request, _('The poll could not be created due to validation errors'))
            edit_handler = EditHandler(instance=poll, form=form)

    else:
        form = EditForm(instance=poll)
        edit_handler = EditHandler(instance=poll, form=form)

    return render(request, 'wagtailpolls/create.html', {
        'form': form,
        'edit_handler': edit_handler,
    })


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def edit(request, poll_pk):
    from ..models import Poll

    poll = get_object_or_404(Poll, pk=poll_pk)

    EditHandler = get_poll_edit_handler(Poll)
    EditForm = EditHandler.get_form_class(Poll)

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=poll)

        if form.is_valid():
            poll = form.save()
            poll.save()
            messages.success(request, _('The poll "{0!s}" has been updated').format(poll))
            return redirect('wagtailpolls_index')

        else:
            messages.error(request, _('The poll could not be updated due to validation errors'))
            edit_handler = EditHandler(instance=poll, form=form)
    else:
        form = EditForm(instance=poll)
        edit_handler = EditHandler(instance=poll, form=form)

    return render(request, 'wagtailpolls/edit.html', {
        'poll': poll,
        'form': form,
        'edit_handler': edit_handler,
    })


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def delete(request, poll_pk):
    from ..models import Poll

    poll = get_object_or_404(Poll, pk=poll_pk)

    if request.method == 'POST':
        poll.delete()
        return redirect('wagtailpolls_index')

    return render(request, 'wagtailpolls/delete.html', {
        'poll': poll,
    })


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def copy(request, poll_pk):
    from ..models import Poll

    poll = Poll.objects.get(id=poll_pk)

    if request.method == 'POST':
        poll.pk = None
        poll.save()
        return redirect('wagtailpolls_index')

    return render(request, 'wagtailpolls/copy.html', {
        'poll': poll,
    })
