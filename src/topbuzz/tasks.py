import requests
from datetime import timedelta
from .models import Channel, Stat
from django.db import transaction


def _stat(start_date, end_date, cookie):
    headers = {
        'pragma': 'no-cache',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'alexatoolbar-alx_ns_ph': 'AlexaToolbar/alx-4.0.1',
        'accept': '*/*',
        'cache-control': 'no-cache',
        'authority': 'topbuzz.com',
        'cookie': cookie,
        'referer': 'https://topbuzz.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }

    if end_date < start_date + timedelta(days=30):
        query_end_date = end_date
    else:
        query_end_date = start_date + timedelta(days=30)

    params = (
        ('start_date', start_date.strftime('%Y-%m-%d 00:00:00')),
        ('end_date', query_end_date.strftime('%Y-%m-%d 00:00:00')),
    )

    data = requests.get('https://topbuzz.com/pgc/daily/stats', headers=headers, params=params).json()['data']
    imprs = data['daily_stats']['author_impression_count']
    clicks = data['daily_stats']['author_go_detail_count']

    if query_end_date == end_date:
        return imprs, clicks

    _imprs, _clicks = _stat(query_end_date + timedelta(days=1), end_date, cookie)

    return imprs + _imprs, clicks + _clicks


@transaction.atomic
def stat(channel, start_date, end_date, cookie):
    dates = [start_date + timedelta(days=k) for k in range((end_date-start_date).days + 1)]
    imprs, clicks = _stat(start_date, end_date, cookie)

    channel, _ = Channel.objects.get_or_create(name=channel)

    for date, impr, click in zip(dates, imprs, clicks):
        Stat.objects.update_or_create(
            channel=channel,
            date=date,
            defaults={
                "recommend": impr,
                "read": click
            }
        )
