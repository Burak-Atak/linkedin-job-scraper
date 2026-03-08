from random import randint

get_random_number = lambda: randint(60 * 60 - 5 * 60, 60 * 60 + 5 * 60)

CELERYBEAT_SCHEDULE = {
    'get_linkedin_jobs-cron_0': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'python developer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_1': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'software developer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_2': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'software engineer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_3': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'python engineer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_4': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'backend engineer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_5': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'backend developer',
            'location_name': 'Türkiye',
            'listed_at': 25 * 60 * 60,
        },
    },
    'get_linkedin_jobs-cron_6': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'python developer',
            'listed_at': 25 * 60 * 60,
            'remote': '2',
            'location_geo_id': '92000000'
        },
    },
    'get_linkedin_jobs-cron_7': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'software developer',
            'listed_at': 25 * 60 * 60,
            'remote': '2',
            'location_geo_id': '92000000'
        },
    },
    'get_linkedin_jobs-cron_8': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'software engineer',
            'listed_at': 25 * 60 * 60,
            'remote': '2',
            'location_geo_id': '92000000'
        },
    },
    'get_linkedin_jobs-cron_9': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'python engineer',
            'listed_at': 25 * 60 * 60,
            'remote': '2',
            'location_geo_id': '92000000'
        },
    },
    'get_linkedin_jobs-cron_10': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'backend engineer',
            'listed_at': 25 * 60 * 60,
            'remote': '2',
            'location_geo_id': '92000000'
        },
    },
    'get_linkedin_jobs-cron_11': {
        'task': 'jobs.tasks.get_linkedin_jobs',  # NOQA
        'schedule': get_random_number(),
        'args': (),
        'kwargs': {
            'keywords': 'backend developer',
            'listed_at': 25 * 60 * 60,
            'remote': '2',
            'location_geo_id': '92000000'
        },
    },

}
