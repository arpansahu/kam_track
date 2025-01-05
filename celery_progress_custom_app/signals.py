from celery.signals import task_postrun, task_revoked
from celery_progress_custom_app.backend import WebSocketProgressRecorder
from .backend import KnownResult, Progress

@task_postrun.connect(retry=True)
def task_postrun_handler(task_id, **kwargs):
    result = KnownResult(task_id, kwargs.pop('retval'), kwargs.pop('state'))
    data = Progress(result).get_info()
    WebSocketProgressRecorder.push_update(task_id, data=data, final=True)

@task_revoked.connect(retry=True)
def task_revoked_handler(request, **kwargs):
    _result = ('terminated' if kwargs.pop('terminated') else None) or ('expired' if kwargs.pop('expired') else None) \
        or 'revoked'
    result = KnownResult(request.id, _result, 'REVOKED')
    data = Progress(result).get_info()
    WebSocketProgressRecorder.push_update(request.id, data=data, final=True)
