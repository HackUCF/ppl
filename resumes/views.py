import csv
import io
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import Group

from django.http import HttpResponse, HttpResponseBadRequest

from django.shortcuts import render

from resumes.forms import ResumeFilterForm
from resumes.models import Resume


def _can_view_resumes(user):
    """
    :type: user User
    """
    if user.is_anonymous():
        return False
    if user.is_staff:
        return True

    grouped = Group.objects.filter(
        share_group__isnull=False) & user.groups.all()
    return grouped.exists()


can_view_resumes = user_passes_test(
    _can_view_resumes,
    login_url=settings.LOGIN_URL + '?reason=no_resume_view_permission'
)


@login_required
@can_view_resumes
def view_resumes(request):
    # only sponsors, guests, and club execs may view
    form, resumes = _search(request)

    return render(request, 'resumes.html', {
        'form': form,
        'resumes': resumes
    })


@login_required
@can_view_resumes
def export_csv(request):
    form, resumes = _search(request)
    if not form.is_valid():
        return HttpResponseBadRequest('Search invalid')

    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(['Name', 'Graduation', 'Submitted', 'URL'])
    for resume in resumes:
        writer.writerow([resume.member.name, resume.get_graduation_display(),
                         resume.timestamp, resume.url])

    resp = HttpResponse(stream.getvalue(), content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename=hackucf_resumes.csv'
    return resp


def _search(request):
    all_grad_dates = len(request.GET.get('graduation', [])) == 0
    form = ResumeFilterForm(request.GET)
    resumes = Resume.objects.select_related('member').order_by('graduation')
    if form.is_valid():
        # filter by user's groups
        if not request.user.is_staff:
            groups = request.user.groups.all()
            resumes = resumes.filter(shared_with__group__in=groups)

        # convert to GRADUATION_CHOICES and filter
        if not all_grad_dates:
            grad_dates = [Resume.GRADUATION_DATES[x] for x in
                          form.cleaned_data['graduation']]
            resumes = resumes.filter(graduation__in=grad_dates)

        # filter submission date
        submission_time = form.cleaned_data['submitted_by']
        if submission_time:
            submission_dt = datetime.combine(submission_time,
                                             datetime.min.time())
            resumes = resumes.filter(timestamp__lte=submission_dt)
    return form, resumes
