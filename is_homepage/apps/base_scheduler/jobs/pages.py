import logging

from django.utils import timezone

from wagtail.models import Page, Revision


logger = logging.getLogger('BaseScheduler')


def publish_unpublish_scheduled_pages_job():
    """
    This job publishes, updates or unpublishes objects that have had these actions scheduled by an editor.
    More info here: https://docs.wagtail.org/en/v5.2.1/reference/management_commands.html#publish-scheduled
    """

    import subprocess
    from ..models import SchedulerHistoryModel

    job_name = 'Scheduled Pages'

    if not SchedulerHistoryModel.should_run_job(job_name):
        logger.info(f'SchedulerJOB:{job_name}: Current job already running.')
        return

    db_job_id = SchedulerHistoryModel.create_db_job(job_name)

    to_publish_all = Revision.objects.filter(approved_go_live_at__isnull=False).count()
    to_unpublish_all = Page.objects.filter(live=True, expire_at__isnull=False).count()

    to_publish_before = Revision.objects.filter(approved_go_live_at__lt=timezone.now()).count()
    to_unpublish_before = Page.objects.filter(live=True, expire_at__lt=timezone.now()).count()

    subprocess.run(['python3', 'manage.py', 'publish_scheduled'])

    to_publish_after = Revision.objects.filter(approved_go_live_at__lt=timezone.now()).count()
    to_unpublish_after = Page.objects.filter(live=True, expire_at__lt=timezone.now()).count()

    notes = (f'Published: {to_publish_before - to_publish_after}/{to_publish_all}' if to_publish_all > 0 else 'Nothing to publish')
    notes += ' | ' + (f'Unpublished: {to_unpublish_before - to_unpublish_after}/{to_unpublish_all}' if to_unpublish_all > 0 else 'Nothing to unpublish')

    SchedulerHistoryModel.complete_db_job(db_job_id, notes)

    logger.info(f'SchedulerJOB:{job_name}: {notes}')
