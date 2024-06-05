import os


def environment_variables(request):

    return {
        'environment_variables': {
            'APP_PRD_URL': 'https://innovation.nhs.uk',
            'ENABLE_ANALYTICS': os.environ.get('ENABLE_ANALYTICS') or False,
            'GTM_ID': os.environ.get('GTM_ID') or '',
            'TAG_MEASUREMENT_ID': os.environ.get('TAG_MEASUREMENT_ID') or '',
        }
    }
