from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import render
from django.utils.decorators import method_decorator

from modelcluster.fields import ParentalKey

from django_ratelimit.decorators import ratelimit

from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField, WagtailAdminFormPageForm

from wagtailnhsukfrontend.blocks import ActionLinkBlock, InsetTextBlock, RichTextBlock

from is_homepage.config.helpers.notifications_helper import send_contact_email


form_constants = {
    # Needed constants relative to mandatory fields that must exist in order to send to different email recipients.
    # "support_type_field_name" refers to the clean name, not the label.
    'support_type_field_name': 'reason_for_contact',
    'support_type_field_general_enquiry_choice': 'General enquiry',
    'support_type_field_technical_support_choice': 'Technical support',
    'support_type_field_event_media_enquiries_choice': 'Event and media enquiries'
}


class FormField(AbstractFormField):
    page = ParentalKey('ContactUsPage', on_delete=models.CASCADE, related_name='form_fields')


class ContactUsAdminPage(WagtailAdminFormPageForm):

    def clean(self):

        super().clean()  # Calls WagtailAdminFormPageForm clean method, that runs basic validations.

        if 'form_fields' in self.formsets:

            has_request_type_field = False

            for field in self.formsets['form_fields'].forms:

                field_clean_name = field.instance.get_field_clean_name()
                field_choices = field.instance.choices

                if field_clean_name == form_constants['support_type_field_name'] and field_choices == f'{ form_constants["support_type_field_general_enquiry_choice"] }, { form_constants["support_type_field_technical_support_choice"] }, { form_constants["support_type_field_event_media_enquiries_choice"] }':
                    has_request_type_field = True

            if not has_request_type_field:
                raise ValidationError('''
                    You must have a mandatory radio-button field called "Reason for contact", with the field choices equal to: "General enquiry, Technical support, Event and media enquiries".
                    These are mandadory to determine the email notifications recipients.
                ''')


class ContactUsPage(AbstractForm):

    template = 'contact_page.html'
    landing_page_template = 'success_landing_page.html'

    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = []

    base_form_class = ContactUsAdminPage

    intro = RichTextField(verbose_name='Introduction', blank=True)

    success_landing_content = StreamField([
        ('rich_text', RichTextBlock()),
        ('action_link', ActionLinkBlock()),
        ('inset_text', InsetTextBlock())
    ], null=True, use_json_field=True)

    general_enquiry_email = models.EmailField(
        null=True,
        blank=False,
        max_length=255,
        help_text='Message will be sent to this email when user chooses "General enquiry" option.'
    )
    technical_support_email = models.EmailField(
        null=True,
        blank=False,
        max_length=255,
        help_text='Message will be sent to this email when user chooses "Technical support" option.'
    )
    event_media_enquiries_email = models.EmailField(
        null=True,
        blank=False,
        max_length=255,
        help_text='Message will be sent to this email when user chooses "Event and media enquiries" option.'
    )

    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('success_landing_content'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('general_enquiry_email', classname='col6'),
                FieldPanel('technical_support_email', classname='col6')
            ]),
            FieldRowPanel([
                FieldPanel('event_media_enquiries_email', classname='col6')
            ])
        ], heading='Email recipients')
    ]

    promote_panels = [
        FieldPanel('slug'),
        FieldPanel('seo_title'),
        FieldPanel('search_description')
    ]

    @method_decorator(ratelimit(key='ip', rate='2/s', block=True), name='serve')
    @method_decorator(ratelimit(key='ip', rate='20/m', block=True), name='serve')
    @method_decorator(ratelimit(key='ip', rate='80/h', block=True), name='serve')
    @method_decorator(ratelimit(key='ip', rate='100/d', block=True), name='serve')
    def serve(self, request):

        if request.method == 'POST':

            form = self.get_form(request.POST)

            if form.is_valid():

                template_data = ''
                for field in self.get_form_fields():
                    template_data += f'\n{ field.label }\n{ form.cleaned_data[field.clean_name] }\n'

                try:
                    if form.cleaned_data[form_constants['support_type_field_name']] == form_constants['support_type_field_general_enquiry_choice']:
                        send_contact_email(self.general_enquiry_email, template_data)
                    elif form.cleaned_data[form_constants['support_type_field_name']] == form_constants['support_type_field_technical_support_choice']:
                        send_contact_email(self.technical_support_email, template_data)
                    elif form.cleaned_data[form_constants['support_type_field_name']] == form_constants['support_type_field_event_media_enquiries_choice']:
                        send_contact_email(self.event_media_enquiries_email, template_data)
                    else:
                        raise AssertionError('Error: Unknown email to send')

                    super(ContactUsPage, self).process_form_submission(form)  # Save form to admin.

                    return render(request, self.landing_page_template, {'page': self})

                except:
                    self.title = f'Error: { self.title }'
                    return render(request, 'error_landing_page.html', {'page': self})

        else:
            form = self.get_form(page=self)

        return render(request, self.template, {'page': self, 'form': form})
    

