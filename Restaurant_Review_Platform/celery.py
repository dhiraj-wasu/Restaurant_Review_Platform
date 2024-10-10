# myproject/celery.py

import os
from celery import Celery
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Restaurant_Review_Platform.settings')
# set the default Django settings module for the 'celery' program.


app = Celery('Restaurant_Review_Platform')

# Using a string here means the worker doesn't 
# have to serialize the configuration object to 
# child processes. - namespace='CELERY' means all 
# celery-related configuration keys should 
# have a `CELERY_` prefix.
app.config_from_object('django.conf:settings',
                       namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['backend.backup'])
app.conf.beat_schedule = {
    'update-leaderboard-every-10-minutes': {
        'task': 'backend.backup.my_function',
        'schedule': crontab(minute='*/1'),  # Run every 10 minutes
        'args': (),
    },
}
