"""
Pharmacy ilovasi uchun view'lar.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Q
from django.http import JsonResponse
from .models import Region, Pharmacy
from apps.medicines.models import Medicine, PharmacyStock


class HomeView(TemplateView):
    """Bosh sahifa."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['regions'] = Region.objects.annotate(
            total_pharmacies=Count('pharmacies', filter=Q(pharmacies__is_active=True))
        ).order_by('name')
        ctx['featured_pharmacies'] = Pharmacy.objects.filter(
            is_active=True, is_verified=True
        ).select_related('region')[:6]
        ctx['total_pharmacies'] = Pharmacy.objects.filter(is_active=True).count()
        ctx['total_medicines'] = Medicine.objects.count()
        ctx['total_regions'] = Region.objects.count()
        ctx['popular_medicines'] = Medicine.objects.annotate(
            stock_count=Count('stock_entries')
        ).order_by('-stock_count')[:8]

        # Xarita uchun barcha dorixonalarning koordinatalari
        pharmacies = Pharmacy.objects.filter(is_active=True).select_related('region')
        ctx['pharmacy_locations'] = [
            {
                'id': p.id,
                'name': p.name,
                'lat': p.latitude,
                'lng': p.longitude,
                'address': p.address,
                'phone': p.phone,
                'region': p.region.name,
                'url': p.get_absolute_url(),
                'is_24h': p.is_24_hours,
            }
            for p in pharmacies
        ]
        return ctx


class PharmacyDetailView(DetailView):
    """Dorixona haqida batafsil ma'lumot."""
    model = Pharmacy
    template_name = 'pharmacies/detail.html'
    context_object_name = 'pharmacy'

    def get_queryset(self):
        return Pharmacy.objects.filter(is_active=True).select_related('region')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['stock_items'] = self.object.stock_items.filter(
            is_available=True, quantity__gt=0
        ).select_related('medicine', 'medicine__category').order_by('medicine__name')

        # Yaqin atrofdagi dorixonalar (shu hududda)
        ctx['nearby_pharmacies'] = Pharmacy.objects.filter(
            region=self.object.region, is_active=True
        ).exclude(id=self.object.id)[:5]
        return ctx


class RegionDetailView(DetailView):
    """Tuman bo'yicha dorixonalar ro'yxati."""
    model = Region
    template_name = 'pharmacies/region_detail.html'
    context_object_name = 'region'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pharmacies'] = self.object.pharmacies.filter(
            is_active=True
        ).order_by('-is_verified', 'name')
        ctx['pharmacy_locations'] = [
            {
                'id': p.id,
                'name': p.name,
                'lat': p.latitude,
                'lng': p.longitude,
                'address': p.address,
                'phone': p.phone,
                'url': p.get_absolute_url(),
                'is_24h': p.is_24_hours,
            }
            for p in ctx['pharmacies']
        ]
        return ctx


class PharmacyListView(ListView):
    """Barcha dorixonalar ro'yxati."""
    model = Pharmacy
    template_name = 'pharmacies/list.html'
    context_object_name = 'pharmacies'
    paginate_by = 20

    def get_queryset(self):
        qs = Pharmacy.objects.filter(is_active=True).select_related('region')
        region_slug = self.request.GET.get('region')
        if region_slug:
            qs = qs.filter(region__slug=region_slug)
        only_24h = self.request.GET.get('only_24h')
        if only_24h:
            qs = qs.filter(is_24_hours=True)
        only_delivery = self.request.GET.get('only_delivery')
        if only_delivery:
            qs = qs.filter(has_delivery=True)
        return qs.order_by('-is_verified', 'name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['regions'] = Region.objects.all().order_by('name')
        ctx['selected_region'] = self.request.GET.get('region', '')
        return ctx
