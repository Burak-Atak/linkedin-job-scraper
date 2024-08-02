from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'get_linkedin_jobs-cron_0': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': crontab(hour='*/2'),
        'args': (),
        'kwargs': {
            'keywords': 'python developer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_1': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': crontab(hour='*/2'),
        'args': (),
        'kwargs': {
            'keywords': 'software developer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_2': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': crontab(hour='*/2'),
        'args': (),
        'kwargs': {
            'keywords': 'software engineer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_3': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': crontab(hour='*/2'),
        'args': (),
        'kwargs': {
            'keywords': 'python engineer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_4': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': crontab(hour='*/2'),
        'args': (),
        'kwargs': {
            'keywords': 'backend engineer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_5': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': crontab(hour='*/2'),
        'args': (),
        'kwargs': {
            'keywords': 'backend developer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
}
