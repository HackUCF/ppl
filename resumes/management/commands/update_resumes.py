import csv

from dateutil.parser import parse as parse_datetime
from dateutil.tz import tzoffset
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from membership import api
from membership.models import Member
from resumes.models import Resume, ResumeShares


class Command(BaseCommand):
    help = 'Updates resume archive from Google Sheets'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-file', default='resumes.csv')
        parser.add_argument('--auth_host_name', default='localhost',
                            help='Hostname when running a local web server.')
        parser.add_argument('--noauth_local_webserver', action='store_true',
                            default=False,
                            help='Do not run a local web server.')
        parser.add_argument('--auth_host_port', default=[8080, 8090], type=int,
                            nargs='*', help='Port web server should listen on.')

    def handle(self, *args, **options):
        output_file = options['output_file']
        self.stdout.write('[+] Exporting resumes to {}'.format(output_file))
        self.download_resumes(options, output_file)
        self.stdout.write('[+] Updating resumes')
        self.update_resumes(output_file)

    @staticmethod
    def download_resumes(options, output_file):
        service = api.build_service(options)
        file = service.files().get(fileId=settings.GOOGLE_RESUME_RESPONSES_FILE_ID).execute()
        url = file['exportLinks']['text/csv']
        resp, content = service._http.request(url)
        open(output_file, 'wb').write(content)

    def update_resumes(self, output_file,
                       timezone=tzoffset('EST', -1 * 5 * 60 * 60)):
        csv_file = open(output_file, 'r', encoding='utf-8')
        reader = csv.reader(csv_file)
        headings = next(reader)
        for row in reader:
            data = dict(zip(headings, row))
            timestamp = parse_datetime(data['Timestamp']).replace(
                tzinfo=timezone)
            knights_email = data['Knights Email']
            planned_graduation = data['Planned Graduation']
            planned_graduation = Resume.GRADUATION_DATES[planned_graduation]
            url = data['Resume Link']
            opted_in = data['Opt-in Resume Sharing']

            self.create_member(knights_email, timestamp, url,
                               planned_graduation, opted_in)
        csv_file.close()

    def create_member(self, knights_email, timestamp, url, graduation_date,
                      opted_in):
        try:
            member = Member.objects.get(knights_email__iexact=knights_email)
        except Member.DoesNotExist:
            self.stdout.write('[-] {} not a member!'.format(knights_email))
            return
        try:
            resume = Resume.objects.get(member=member)
            resume.timestamp = timestamp
            resume.url = url
            resume.graduation = graduation_date
        except Resume.DoesNotExist:
            resume = Resume(timestamp=timestamp, member=member, url=url,
                            graduation=graduation_date)
        resume.save()

        for party_name in opted_in.split(', '):
            group, _ = Group.objects.get_or_create(name=party_name)
            party, _ = ResumeShares.objects.get_or_create(group=group)
            resume.shared_with.add(party)
