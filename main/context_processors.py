from .models import Page, SiteSetting


def site_context(request):
    """Injects nav pages and site settings into every template context."""
    return {
        'nav_pages':     Page.objects.filter(is_published=True, show_in_nav=True).order_by('nav_order'),
        'site_settings': SiteSetting.get(),
    }
