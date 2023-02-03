import os


def environment_variables(request):

    return {
        'environment_variables': {
            'ENABLE_ANALYTICS': os.environ.get('ENABLE_ANALYTICS') == 'true' or False
        }
    }
