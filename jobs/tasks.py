from linkedin.celery import app
from django.core.cache import cache
from jobs.service import JobsService
from datetime import datetime, timedelta
import logging
from celery.exceptions import SoftTimeLimitExceeded
from functools import wraps

logger = logging.getLogger(__name__)

TIMEOUT = 3600 * 3


def unique_task(callback, *decorator_args, **decorator_kwargs):
    """
    Decorator to ensure only one instance of the task is running at once.
    """

    @wraps(callback)
    def _wrapper(*args, **kwargs):
        task_name = [task for task in app.tasks if callback.__name__ in task][0]
        task = app.tasks[task_name]

        active_queues = task.app.control.inspect().active()
        if active_queues:
            for queue in active_queues:
                for running_task in active_queues[queue]:
                    if task.name == running_task['name'] and task.request.id != running_task['id']:
                        return f'Task "{callback.__name__}()" cancelled! already running...'

        return callback(*args, **kwargs)

    return _wrapper


@app.task(time_limit=TIMEOUT, soft_time_limit=TIMEOUT)
@unique_task
def get_linkedin_jobs(*args, **kwargs):
    force = kwargs.get('force', False)
    keywords = kwargs.get('keywords')
    formatted_keywords = keywords.replace(' ', '_').lower()
    last_run_datetime = cache.get(f'{formatted_keywords}_last_run_datetime') or datetime.now() - timedelta(
        days=7)
    last_run_diff = datetime.now() - last_run_datetime

    if not force:
        is_runnable = last_run_diff > timedelta(days=1)
        if not is_runnable:
            logger.info(f"Last run was {last_run_datetime}. Skipping this run.")
            return
    try:
        logger.info(f"Starting linkedin scraping for '{keywords}'")

        limit = int(kwargs.get('limit', 25))
        offset = int(kwargs.get('offset', 0))
        location_name = kwargs.get('location_name')
        listed_at = int(kwargs.get('listed_at', 0))

        job_service = JobsService()

        last_run_diff_in_seconds = last_run_diff.total_seconds()
        listed_at = int(max(listed_at, last_run_diff_in_seconds)) + 3600
        new_run_datetime = datetime.now()

        while True:
            is_continue = job_service.scrape_jobs(keywords, limit=limit, offset=offset,
                                                  location_name=location_name,
                                                  listed_at=listed_at)
            if not is_continue:
                break
            offset += limit

        cache.set(f'{formatted_keywords}_last_run_datetime', new_run_datetime, timeout=None)
        logger.info("****************** Linkedin scraping completed ******************")


    except SoftTimeLimitExceeded:
        logger.warning("Task exceeded soft time limit.")
