import http

from celery.schedules import crontab
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from celery import current_app


class TaskView(APIView):
    def get(self, request):
        tasks = current_app.tasks
        app_tasks = [task for task in tasks if not task.startswith('celery.')]

        return Response({'tasks': app_tasks})

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        task = request.data.get('task')
        args = request.data.get('args', [])
        kwargs = request.data.get('kwargs', {})

        tasks = current_app.tasks
        task = tasks.get(task)

        if task:
            task.delay(*args, **kwargs)
        else:
            return Response({'status': 'error', 'message': 'Task not found'}, status=http.HTTPStatus.BAD_REQUEST)

        return Response({'status': 'ok'})


class CronJobsView(APIView):
    @staticmethod
    def _serialize_schedule(schedule):
        if isinstance(schedule, (int, float)):
            return {
                'type': 'interval',
                'every_seconds': schedule,
            }

        if isinstance(schedule, crontab):
            return {
                'type': 'crontab',
                'minute': str(schedule.minute),
                'hour': str(schedule.hour),
                'day_of_week': str(schedule.day_of_week),
                'day_of_month': str(schedule.day_of_month),
                'month_of_year': str(schedule.month_of_year),
            }

        return {
            'type': schedule.__class__.__name__ if schedule else None,
            'value': str(schedule) if schedule is not None else None,
        }

    def get(self, request):
        beat_schedule = current_app.conf.beat_schedule or {}
        jobs = []

        for name, entry in beat_schedule.items():
            if not entry.get('enabled', True):
                continue

            jobs.append({
                'name': name,
                'task': entry.get('task'),
                'schedule': self._serialize_schedule(entry.get('schedule')),
                'args': list(entry.get('args') or []),
                'kwargs': entry.get('kwargs') or {},
                'options': entry.get('options') or {},
            })

        return Response({'count': len(jobs), 'results': jobs})
