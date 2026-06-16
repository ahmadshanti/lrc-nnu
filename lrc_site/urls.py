from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # Language-switching — outside i18n_patterns
    path('i18n/', include('django.conf.urls.i18n')),
    # Admin — outside i18n_patterns (always at /admin/ regardless of language)
    path('admin/', admin.site.urls),
    # Root redirect → Arabic home
    path('', RedirectView.as_view(url='/ar/', permanent=False)),
    # Redirect /ar/admin/ and /en/admin/ → /admin/
    path('ar/admin/', RedirectView.as_view(url='/admin/', permanent=False)),
    path('en/admin/', RedirectView.as_view(url='/admin/', permanent=False)),
]

urlpatterns += i18n_patterns(
    path('', include('main.urls', namespace='main')),
    prefix_default_language=True,   # /ar/ and /en/ both explicit — no ambiguity
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
