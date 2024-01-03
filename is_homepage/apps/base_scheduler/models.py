import logging
import signal
import sys
import threading

from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.conf import settings

from .jobs import health_cleanup_job, health_check_job, publish_unpublish_scheduled_pages_job
from .constants import SchedulerHistoryModelStatus
from .helpers import is_main_runtime_process
from .scheduler import BaseScheduler

scheduler_enabled = getattr(settings, 'BASE_SCHEDULER_ENABLED', False)

logger = logging.getLogger('BaseScheduler')


# Models.
class SchedulerHistoryModel(models.Model):

    name = models.CharField(null=False, blank=False, max_length=50)
    status = models.CharField(null=False, blank=False, max_length=25, choices=SchedulerHistoryModelStatus.choices, default=SchedulerHistoryModelStatus.STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True, max_length=255)

    @staticmethod
    def should_run_job(name):
        """
        To prevent duplicated runs (ex: if the app service scales in the PRD environment, creating multiple instances), this method checks if the same job ran in the last 15 minutes.
        WARNING: This means that no job should be scheduled to run below a 15 minute recurrence.
        """
        fifteen_minutes_ago = timezone.now().replace(microsecond=0) - timedelta(minutes=15)
        return SchedulerHistoryModel.objects.filter(name=name, created_at__gt=fifteen_minutes_ago).count() == 0

    @staticmethod
    def create_db_job(name):
        db_record = SchedulerHistoryModel.objects.create(name=name, status=SchedulerHistoryModelStatus.STARTED)
        return db_record.id

    @staticmethod
    def complete_db_job(id, notes=None):
        try:
            db_record = SchedulerHistoryModel.objects.get(id=id)
            db_record.status = SchedulerHistoryModelStatus.COMPLETED
            db_record.completed_at = timezone.now().replace(microsecond=0)
            db_record.notes = notes
            db_record.save()
        except Exception as e:
            logger.error(f'Unable to save job status update: {e}')

    def __str__(self):
        return f'{self.name} ({self.id})'

    class Meta():
        verbose_name = 'Scheduler History'
        verbose_name_plural = 'Scheduler History'
        db_table = 'scheduler_history_model'


# Scheduler runtime.
stop_run_continuously = threading.Event()

if scheduler_enabled and is_main_runtime_process():

    logger.info('Starting scheduler')
    scheduler = BaseScheduler()

    # Publish unpublish job. Runs every hour at minute 01.
    scheduler.every().hour.at(':54').do(publish_unpublish_scheduled_pages_job)

    # Health check job. Runs every hour at minute 05.
    scheduler.every().hour.at(':55').do(health_check_job)

    # Health cleanup job. Runs every day.
    scheduler.every().day.at('03:00').do(health_cleanup_job)

    stop_run_continuously = scheduler.run_continuously()

    # Mainly for local development, catch interrupt keyboard command and stop running threads and processes.
    # More information about signals: https://docs.python.org/3/library/signal.html
    def handler(signum, frame):
        logger.info('Gracefully stopping scheduler thread and processes')
        stop_run_continuously.set()
        sys.exit(130)

    signal.signal(signal.SIGINT, handler)
