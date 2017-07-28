# -*- encoding=utf8 -*-

from django.core.management.base import BaseCommand
from datetime import timedelta, datetime
from topbuzz.tasks import stat
import argparse


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

class Command(BaseCommand):
    help = 'create campaign'

    def add_arguments(self, parser):
        parser.add_argument('channel', type=str)
        parser.add_argument('start_date', type=valid_date)
        parser.add_argument('end_date', type=valid_date)
        parser.add_argument('cookie', type=str)

    def handle(self, *args, **kwargs):
        print stat(kwargs['channel'], kwargs['start_date'], kwargs['end_date'], kwargs['cookie'])
