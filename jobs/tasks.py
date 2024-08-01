from linkedin.celery import app
from django.core.cache import cache
from jobs.service import JobsService


@app.task
def get_linkedin_jobs(*args, **kwargs):
    keywords = kwargs.get('keywords')
    limit = int(kwargs.get('limit'))
    offset = int(kwargs.get('offset'))
    location_name = kwargs.get('location_name')
    listed_at = int(kwargs.get('listed_at'))

    job_service = JobsService()

    while True:
        is_continue = job_service.scrape_jobs(keywords, limit=limit, offset=offset, location_name=location_name,
                                              listed_at=listed_at)
        if not is_continue:
            break
        offset += limit
