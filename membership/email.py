import mailchimp
from web.models import Member


def sync_mailchimp(api_key, members):
    """
    :param api_key:
    :param members:
    :type members: list[Member]
    :return: list of new subscribers
    """
    api = mailchimp.Mailchimp(api_key)

    # get main subscriber list
    data = api.lists.list()
    mailing_list = next(filter(
        lambda x: x['name'] == 'Collegiate Cyber Defense Club Newsletter',
        data['data']))

    batch = []
    for member in members:
        batch.append({
            'email': {
                'email': member.preferred_email
            }
        })

    resp = api.lists.batch_subscribe(mailing_list['id'], batch)
    newly_subscribed = [x['email'] for x in resp['adds']]
    return newly_subscribed
