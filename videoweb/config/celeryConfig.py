import celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

app = celery.Celery(main="videoweb", broker='redis://localhost:6379/2')

app.autodiscover_tasks(['app.tasks'])