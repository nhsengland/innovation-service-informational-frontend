from wagtail.models import Page


class HomePage(Page):

    template = 'home/home_page.html'
    max_count = 1
    subpage_types = [
        'contact_us.ContactUsPage',
        'innovation_pathway.InnovationPathwayIndexPage'
    ]

    class Meta:
        verbose_name = 'Home page'
        verbose_name_plural = 'Home pages'
