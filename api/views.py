import http

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
