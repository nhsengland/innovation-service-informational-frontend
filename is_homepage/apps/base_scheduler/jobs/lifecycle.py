import logging
import threading

from datetime import timedelta
from django.utils import timezone

from ..constants import SchedulerHistoryModelStatus


logger = logging.getLogger('BaseScheduler')


def cancel_stale_jobs():

    from ..models import SchedulerHistoryModel

    job_name = 'Health Check'

    if not SchedulerHistoryModel.should_run_job(job_name):
        logger.info(f'SchedulerJOB:{job_name}: Current job already running.')
        return

    # Cancel any previous pending job created more than an hour ago.
    one_hour_ago = timezone.now().replace(microsecond=0) - timedelta(hours=1)
    db_pending_jobs_number = (
        SchedulerHistoryModel.objects
        .filter(created_at__lt=one_hour_ago)
        .exclude(status__in=[SchedulerHistoryModelStatus.COMPLETED, SchedulerHistoryModelStatus.TIMEOUT])
        .update(status=SchedulerHistoryModelStatus.TIMEOUT, completed_at=timezone.now().replace(microsecond=0))
    )

    notes = f'Active threads: {threading.active_count()} {[thread.name for thread in threading.enumerate()]}'
    notes += ' | ' + (f'Warning: {db_pending_jobs_number} jobs cancelled' if db_pending_jobs_number > 0 else 'No pending jobs detected')

    # Save job report.
    SchedulerHistoryModel(
        name=job_name,
        status=SchedulerHistoryModelStatus.COMPLETED,
        completed_at=timezone.now().replace(microsecond=0),
        notes=notes
    ).save()

    logger.info(f'SchedulerJOB:{job_name}: {notes}')


def delete_expired_job_history():

    from ..models import SchedulerHistoryModel

    job_name = 'Health Cleanup'

    if not SchedulerHistoryModel.should_run_job(job_name):
        logger.info(f'SchedulerJOB:{job_name}: Current job already running.')
        return

    db_job_id = SchedulerHistoryModel.create_db_job(job_name)

    # Delete jobs older than 6 months.
    six_months_ago = timezone.now().replace(microsecond=0) - timedelta(hours=4320)
    db_pending_jobs_number = SchedulerHistoryModel.objects.filter(created_at__lt=six_months_ago).delete()

    notes = f'{db_pending_jobs_number[0]} rows deleted' if db_pending_jobs_number[0] > 0 else None

    SchedulerHistoryModel.complete_db_job(db_job_id, notes)

    logger.info(f'SchedulerJOB:{job_name}: {notes}')
