from django.core.management.base import BaseCommand

from membership import api
from membership.email import sync_mailchimp
from membership.models import update_membership


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Command(BaseCommand):
    help = 'Updates membership from Google Sheets and syncs with Mailchimps'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mailchimp-api-key',
                            help='Updates the mailing list when provided')
        parser.add_argument('-o', '--output-file', default='membership.csv')
        parser.add_argument('--auth_host_name', default='localhost',
                            help='Hostname when running a local web server.')
        parser.add_argument('--noauth_local_webserver', action='store_true',
                            default=False,
                            help='Do not run a local web server.')
        parser.add_argument('--auth_host_port', default=[8080, 8090], type=int,
                            nargs='*', help='Port web server should listen on.')
        parser.add_argument('--logging-level', default='ERROR')

    def handle(self, *args, **options):
        output_file = options['output_file']
        self.stdout.write('[+] Exporting membership to {}'.format(output_file))
        api.download_membership_file(AttrDict(options), output_file)
        self.stdout.write('[+] Updating membership database...')
        members = update_membership(output_file)
        if options['mailchimp_api_key']:
            print('[+] Updating Mailchimp list...')
            added = sync_mailchimp(options['mailchimp_api_key'], members)
            print('[+] Added {} subscribers (need confirmation)'.format(
                len(added)))
