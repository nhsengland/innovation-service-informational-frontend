def header_navigation_menus(request):
    return {
        'header_navigation_menus': [
            {
                'id': 'developers-guidance',
                'label': 'Developers guidance',
                'slug': '/developers-guidance',
                'description': 'description text',
                'children': [
                    {
                        'label': 'inner item 01',
                        'slug': '/inner',
                        'description': 'Description about item 01'
                    },
                    {
                        'label': 'inner item 02',
                        'slug': '/inner',
                        'description': 'Description about item 02'
                    }

                ]

            },
            {
                'label': 'Adopters guidance',
                'slug': '/adopters-guidance'
            },
            {
                'label': 'Advice services',
                'slug': '/advice-services'
            },
            {
                'label': 'Resources',
                'slug': '/resources'
            },
            {
                'label': 'About this service',
                'slug': '/about-this-service'
            },
        ]
    }


def footer_links(request):
    return {
        'footer_links': [
            {
                'label': 'Accessibility statement',
                'slug': 'accessibility-statement'
            },
            {
                'label': 'Contact us',
                'slug': 'contact-us'
            },
            {
                'label': 'Cookies',
                'slug': 'cookies'
            },
            {
                'label': 'Privacy policy',
                'slug': 'privacy-policy'
            },
            {
                'label': 'Terms and conditions',
                'slug': 'terms-and-conditions'
            }
        ]
    }
