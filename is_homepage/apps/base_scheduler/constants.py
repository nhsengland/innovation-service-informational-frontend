from django.db import models


class SchedulerHistoryModelStatus(models.TextChoices):
    STARTED = 'STARTED', 'Started'
    COMPLETED = 'COMPLETED', 'Completed'
    ERROR = 'ERROR', 'Error'
    TIMEOUT = 'TIMEOUT', 'Timeout'
