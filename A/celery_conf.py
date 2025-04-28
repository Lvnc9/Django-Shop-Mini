from celery import Celery
from datetime import timedelta
import os

### celery automate, manage and locate tasks and me them customized
# by the amount of time running;
# database, input_format, output format, number of workers(aka: cpu cores),

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "A.settings")                 # it's a dictionary of system variables of os


celery_app = Celery("A")
### automatically searches through dirs to locate tasks.py

celery_app.autodiscover_tasks()

# url of borker
celery_app.conf.broken_url = "amqp://"
# how to return resluts (for rabitmq)
celery_app.conf.result_backend = "rpc://"
# we may want to move the tasks from client and server to each other we send them with this specified format
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "pickle"
# what kind of data are allowed to stream:
celery_app.conf.accept_content = ['json', 'pickle']
# how much time a tasks has to finish. if it passes the limit. it get's terminated
celery_app.conf.result_expiers = timedelta(days=1)
# specifies to block a client while running a task or not.
celery_app.conf.task_always_eager = False
# how many tasks each worker can do as parallel. if you have heavy tasks, set it to 4. but if it isn't set it to 1  
celery_app.conf.worker_prefetch_multiplier = 4          # default 4