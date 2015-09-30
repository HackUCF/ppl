#!/usr/bin/env python3

import argparse

from oauth2client import tools

from membership import api, email
from web.models import syncdb, update_membership


def _update(args):
    ACTION_MAP['export'](args)
    members = update_membership(args.output_file)
    if args.mailchimp_api_key:
        email.sync_mailchimp(args.mailchimp_api_key, members)

ACTION_MAP = {
    'export': lambda args: api.download_membership_file(args, args.output_file),
    'update': _update,
    'syncdb': lambda args: syncdb()
}


def main():
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('action', choices=ACTION_MAP.keys())
    parser.add_argument('-m', '--mailchimp-api-key',
                        help='Updates the mailing list when provided')
    parser.add_argument('-o', '--output-file', default='membership.csv')

    args = parser.parse_args()
    ACTION_MAP[args.action](args)


if __name__ == '__main__':
    main()
