import os


def environment_variables(request):

    return {
        'environment_variables': {
            'APP_PRD_URL': 'https://innovation.nhs.uk',
            'ENABLE_ANALYTICS': os.environ.get('ENABLE_ANALYTICS') == 'true'
        }
    }
