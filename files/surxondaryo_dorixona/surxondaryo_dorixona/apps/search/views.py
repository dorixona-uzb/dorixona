"""
Asosiy qidiruv view'i — dori, dorixona va manzil bo'yicha qidiruv.
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q, Min, Count, F
from django.core.paginator import Paginator

from apps.pharmacies.models import Pharmacy, Region
from apps.medicines.models import Medicine, PharmacyStock, MedicineCategory
from .models import SearchHistory


class SearchView(TemplateView):
    """Asosiy qidiruv sahifasi.

    Foydalanuvchi dori nomini kiritsa, uni sotadigan dorixonalarni
    narx, masofa va mavjudlik bo'yicha tartiblab ko'rsatadi.
    """
    template_name = 'search/results.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        query = self.request.GET.get('q', '').strip()
        region_slug = self.request.GET.get('region', '').strip()
        only_24h = self.request.GET.get('only_24h') == '1'
        only_delivery = self.request.GET.get('only_delivery') == '1'
        only_no_prescription = self.request.GET.get('no_rx') == '1'
        max_price = self.request.GET.get('max_price', '').strip()

        # Foydalanuvchi koordinatalari (ixtiyoriy)
        try:
            user_lat = float(self.request.GET.get('lat', ''))
            user_lng = float(self.request.GET.get('lng', ''))
        except (ValueError, TypeError):
            user_lat, user_lng = None, None

        ctx['query'] = query
        ctx['selected_region'] = region_slug
        ctx['only_24h'] = only_24h
        ctx['only_delivery'] = only_delivery
        ctx['only_no_prescription'] = only_no_prescription
        ctx['max_price'] = max_price
        ctx['user_lat'] = user_lat
        ctx['user_lng'] = user_lng
        ctx['regions'] = Region.objects.all().order_by('name')
        ctx['categories'] = MedicineCategory.objects.filter(parent__isnull=True)

        # Bo'sh so'rov bo'lsa
        if not query:
            ctx['stock_results'] = []
            ctx['matched_medicines'] = []
            return ctx

        # 1) Dori-darmonlardan qidirish (nom, INN, manufacturer)
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) |
            Q(generic_name__icontains=query) |
            Q(manufacturer__icontains=query) |
            Q(barcode__iexact=query)
        )
        if only_no_prescription:
            medicines = medicines.filter(prescription_required=False)

        # 2) Topilgan dorilar uchun zaxiralarni olish
        stock_qs = PharmacyStock.objects.filter(
            medicine__in=medicines,
            is_available=True,
            quantity__gt=0,
            pharmacy__is_active=True,
        ).select_related('medicine', 'pharmacy', 'pharmacy__region', 'medicine__category')

        if region_slug:
            stock_qs = stock_qs.filter(pharmacy__region__slug=region_slug)
        if only_24h:
            stock_qs = stock_qs.filter(pharmacy__is_24_hours=True)
        if only_delivery:
            stock_qs = stock_qs.filter(pharmacy__has_delivery=True)
        if max_price:
            try:
                stock_qs = stock_qs.filter(price__lte=float(max_price))
            except ValueError:
                pass

        # 3) Masofa hisoblash (agar koordinata berilgan bo'lsa)
        results = list(stock_qs)
        if user_lat is not None and user_lng is not None:
            for stock in results:
                stock.distance = stock.pharmacy.distance_to(user_lat, user_lng)
            sort_by = self.request.GET.get('sort', 'distance')
            if sort_by == 'distance':
                results.sort(key=lambda x: x.distance)
            elif sort_by == 'price':
                results.sort(key=lambda x: x.price)
        else:
            sort_by = self.request.GET.get('sort', 'price')
            if sort_by == 'price':
                results.sort(key=lambda x: x.price)

        ctx['sort_by'] = sort_by

        # Eng arzon narxni belgilash
        if results:
            min_price = min(r.price for r in results)
            for r in results:
                r.is_cheapest = (r.price == min_price)

        # Paginatsiya
        paginator = Paginator(results, 20)
        page_number = self.request.GET.get('page', 1)
        ctx['page_obj'] = paginator.get_page(page_number)
        ctx['stock_results'] = ctx['page_obj']
        ctx['total_results'] = len(results)

        # Topilgan dorilar (yuqorida ko'rsatish uchun)
        ctx['matched_medicines'] = medicines[:5]

        # Qidiruv tarixini saqlash
        if query:
            SearchHistory.objects.create(
                user=self.request.user if self.request.user.is_authenticated else None,
                query=query,
                region=Region.objects.filter(slug=region_slug).first() if region_slug else None,
                results_count=len(results),
                user_lat=user_lat,
                user_lng=user_lng,
                ip_address=self._get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')[:300],
            )

        return ctx

    def _get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return self.request.META.get('REMOTE_ADDR')
