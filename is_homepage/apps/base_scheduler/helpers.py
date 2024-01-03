import psutil
import sys


def is_main_runtime_process():
    """
    When running locally, Django uses two processes for the reloading feature (to restart on code change).
    Also everytime that "manage.py" is executed, the entire code runs.
    This method will identify the main process/thread in order to run specific code only once.

    Algorithm:
    1. "manage.py runserver" command with specific argument "runserver" was issued. This avoids running scheduler when executing migrations (ex: manage.py migrate)
    2. Even with more than 1 proccess running, detects the one launch by the terminal or a script as this is the MainThread.
       To avoid launching 2 processes you can use the --noreload argument, (manage.py runserver --noreload). This will NOT autoreload on code changes.
    """

    command_arguments = sys.argv
    current_process = psutil.Process()
    parent_process = psutil.Process(current_process.ppid())

    # When running locally, 'bash' or 'sh' is the parent.name. On azure environments, this will be 'startup.sh' script.
    return 'runserver' in command_arguments and parent_process.name() in ['bash', 'sh', 'startup.sh']
