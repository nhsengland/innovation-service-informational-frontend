def header_navigation_menus(request):
    return {
        'header_navigation_menus': [
            {
                'label': 'Get support',
                'description': 'Further information on innovator support',
                'children': [
                    {
                        'label': 'Innovation service',
                        'slug': '/innovation-service',
                        'description': 'Get personalised support'
                    },
                    {
                        'label': 'Innovation pathway',
                        'slug': '/innovation-pathway',
                        'description': 'Get detailed information to help plan ahead'
                    },
                    {
                        'label': 'Funding and programmes',
                        'slug': '/funding-and-programmes',
                        'description': 'Find potential funding partners'
                    }
                ]

            },
            {
                'label': 'News',
                'slug': '/news'
            },
            {
                'label': 'Case studies',
                'slug': '/case-studies'
            },
            {
                'label': 'About us',
                'slug': '/about-us'
            }
        ]
    }


def footer_links(request):
    return {
        'footer_links': [
            {
                'label': 'Accessibility statement',
                'slug': '/accessibility-statement'
            },
            {
                'label': 'Contact us',
                'slug': '/contact-us'
            },
            {
                'label': 'Cookies',
                'slug': '/cookies'
            },
            {
                'label': 'Privacy policy',
                'slug': '/privacy-policy'
            },
            {
                'label': 'Terms and conditions',
                'slug': '/terms-and-conditions'
            }
        ]
    }
