import json

from django.conf import settings

from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache
from django.forms import model_to_dict
from django.http import HttpResponseBadRequest, HttpResponse, \
    HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_safe, require_POST

from membership.api import download_sheet_with_user, user_can_download_sheet
from membership.forms import SearchForm
from membership.models import Member, update_membership

user_can_view_members = user_passes_test(
    lambda u: user_can_download_sheet(u),
    login_url=settings.LOGIN_URL + '?reason=no_member_view_permission'
)


def index(request):
    return render(request, 'index.html')


@login_required
@user_can_view_members
@require_safe
def dashboard(request):
    return render(request, 'dashboard.html', {
        'form': SearchForm(),
        'enable_member_update': cache.get('enable_member_update', True)
    })


@login_required
@user_can_view_members
@require_POST
def search(request):
    form = SearchForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(content=form.errors)

    knights_email = form.cleaned_data['knights_email']
    members = Member.objects.filter(knights_email__contains=knights_email)[:20]
    data = json.dumps({
        'results': {
            'data': [model_to_dict(m) for m in members]
        }
    }, cls=DjangoJSONEncoder)

    return HttpResponse(data, content_type='application/json')


@login_required
@user_can_view_members
@require_POST
def update(request):
    if not request.is_ajax():
        return HttpResponseBadRequest('Must be requested from page')

    filename = 'membership.csv'
    if not download_sheet_with_user(request.user, filename):
        return HttpResponseForbidden('User cannot see the sheet 👎')

    update_membership(filename)

    cache.set('enable_member_update', False, 300)
    # thumbs up unicode
    return HttpResponse('👍')
