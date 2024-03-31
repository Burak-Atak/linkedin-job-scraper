from django.core.management.base import BaseCommand, CommandError
from jobs.service import JobsService


class Command(BaseCommand):
    help = 'Fetch jobs from linkedin'

    def add_arguments(self, parser):
        parser.add_argument('--keywords', nargs='?', default='python')
        parser.add_argument('--limit', nargs='?', default=25)
        parser.add_argument('--offset', nargs='?', default=0)
        parser.add_argument('--listed_at', nargs='?', default=24 * 60 * 60)
        parser.add_argument('--location_name', nargs='?', default=None)

    def handle(self, *args, **options):
        keywords = options.get('keywords')
        limit = int(options.get('limit'))
        offset = int(options.get('offset'))
        location_name = options.get('location_name')
        listed_at = int(options.get('listed_at'))

        job_service = JobsService()

        while True:
            is_continue = job_service.scrape_jobs(keywords, limit=limit, offset=offset, location_name=location_name,
                                                  listed_at=listed_at)
            if not is_continue:
                break
            offset += limit
