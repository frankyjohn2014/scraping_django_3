from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraping_service.settings")
app = Celery("scraping_django_3")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request:{0!n}'.format(self.request))
