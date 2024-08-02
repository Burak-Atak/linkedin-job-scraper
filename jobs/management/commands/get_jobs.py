from django.core.management.base import BaseCommand
from jobs.tasks import get_linkedin_jobs


class Command(BaseCommand):
    help = 'Fetch jobs from linkedin'

    def add_arguments(self, parser):
        parser.add_argument('--keywords', nargs='?', default='python')
        parser.add_argument('--limit', nargs='?', default=25)
        parser.add_argument('--offset', nargs='?', default=0)
        parser.add_argument('--listed_at', nargs='?', default=24 * 60 * 60)
        parser.add_argument('--location_name', nargs='?', default=None)
        parser.add_argument('--force', action='store_true', help='Force the operation.')

    def handle(self, *args, **kwargs):
        get_linkedin_jobs.delay(*args, **kwargs)
