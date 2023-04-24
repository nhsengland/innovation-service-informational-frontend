import os

from notifications_python_client.notifications import NotificationsAPIClient

from is_homepage.config.constants.constants import NOTIFICATIONS


def __generate_api_key():
    return NotificationsAPIClient(
        f'{ os.environ.get("EMAIL_NOTIFICATION_API_ISSUER") }-{ os.environ.get("EMAIL_NOTIFICATION_API_SECRET") }',
        os.environ.get("EMAIL_NOTIFICATION_API_BASE_URL")
    )


def send_contact_email(email_address, data):

    client = __generate_api_key()

    response = client.send_email_notification(
        email_address=email_address,
        template_id=NOTIFICATIONS['contact_us_template_id'],
        personalisation={'data': data},
        reference=None,
        email_reply_to_id=None
    )

    return response
