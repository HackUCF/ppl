import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe, require_POST
from membership.forms import SearchForm
from membership.models import Member


@require_safe
def dashboard(request):
    return render(request, 'index.html', {
        'form': SearchForm()
    })


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