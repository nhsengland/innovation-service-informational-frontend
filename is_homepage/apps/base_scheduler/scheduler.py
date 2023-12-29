import datetime
import logging
import threading
import time
from schedule import Scheduler


logger = logging.getLogger('BaseScheduler')


class BaseScheduler(Scheduler):
    """
    Custom implementation of scheduler (https://schedule.readthedocs.io) that allows:
    1. Make scheduler run on a autonomous thread so it don't block wagtail runtime.
    2. Catch jobs that fail and logs their exception tracebacks as errors, and optionally reschedules jobs for their next run time.

    This method allows to run jobs that may or may not crash without worrying about whether other jobs will run or if they'll crash the entire script.
    """

    def __init__(self, reschedule_on_failure=True):
        """
        If reschedule_on_failure is True, jobs will be rescheduled for their next run as if they had completed successfully.
        If False, they'll run on the next run_pending() tick.
        """

        self.reschedule_on_failure = reschedule_on_failure
        super().__init__()

    def _run_job(self, job):

        try:
            super()._run_job(job)
        except Exception as e:
            job.last_run = datetime.datetime.now()
            job._schedule_next_run()
            logger.error(f'ERROR\n${format(e)}')

    def run_continuously(self, interval=1):
        """
        Continuously run, while executing pending jobs at each elapsed time interval.

        @return cease_continuous_run: threading.Event which can be set to cease continuous run.

        Please note that it is *intended behavior that run_continuously() does not run missed jobs*.
        For example, if you've registered a job that should run every minute and you set a continuous run interval of one hour then your job won't be run 60 times at each interval but only once.
        """

        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):

            def __init__(self):
                super().__init__(name='SchedulerThread')

            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    self.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()

        logger.info('Scheduler thread successfully started!')

        return cease_continuous_run
