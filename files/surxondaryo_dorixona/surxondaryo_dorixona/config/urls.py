"""
Surxondaryo Dorixona — URL routing
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.pharmacies.urls')),
    path('medicine/', include('apps.medicines.urls')),
    path('search/', include('apps.search.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('api/', include('apps.api.urls')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin sayt sarlavhalari
admin.site.site_header = "Surxondaryo Dorixona — Boshqaruv paneli"
admin.site.site_title = "Surxondaryo Dorixona"
admin.site.index_title = "Tizim boshqaruvi"
