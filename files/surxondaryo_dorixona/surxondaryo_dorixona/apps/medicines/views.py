"""Dorilar uchun view'lar."""
from django.views.generic import DetailView, ListView
from django.db.models import Min, Count, Q
from .models import Medicine, MedicineCategory, PharmacyStock


class MedicineDetailView(DetailView):
    """Dori haqida batafsil ma'lumot va u sotiladigan dorixonalar."""
    model = Medicine
    template_name = 'medicines/detail.html'
    context_object_name = 'medicine'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        stock_qs = self.object.stock_entries.filter(
            is_available=True, quantity__gt=0
        ).select_related('pharmacy', 'pharmacy__region').order_by('price')

        # Tuman bo'yicha filtrlash
        region_slug = self.request.GET.get('region')
        if region_slug:
            stock_qs = stock_qs.filter(pharmacy__region__slug=region_slug)

        ctx['stock_items'] = stock_qs
        ctx['min_price'] = stock_qs.aggregate(min_price=Min('price'))['min_price']
        ctx['cheapest_stock'] = stock_qs.first() if stock_qs.exists() else None

        # O'xshash dorilar (bir xil turkumdan)
        if self.object.category:
            ctx['similar_medicines'] = Medicine.objects.filter(
                category=self.object.category
            ).exclude(id=self.object.id)[:6]
        else:
            ctx['similar_medicines'] = []
        return ctx


class MedicineListView(ListView):
    """Barcha dorilar ro'yxati va filtrlash."""
    model = Medicine
    template_name = 'medicines/list.html'
    context_object_name = 'medicines'
    paginate_by = 24

    def get_queryset(self):
        qs = Medicine.objects.annotate(
            stock_count=Count('stock_entries', filter=Q(stock_entries__is_available=True))
        ).filter(stock_count__gt=0).select_related('category')

        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        prescription = self.request.GET.get('prescription')
        if prescription == 'no':
            qs = qs.filter(prescription_required=False)
        elif prescription == 'yes':
            qs = qs.filter(prescription_required=True)

        return qs.order_by('name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = MedicineCategory.objects.filter(parent__isnull=True).annotate(
            med_count=Count('medicines')
        )
        ctx['selected_category'] = self.request.GET.get('category', '')
        return ctx


class CategoryDetailView(ListView):
    """Turkum bo'yicha dorilar."""
    template_name = 'medicines/category.html'
    context_object_name = 'medicines'
    paginate_by = 24

    def get_queryset(self):
        self.category = MedicineCategory.objects.get(slug=self.kwargs['slug'])
        return Medicine.objects.filter(category=self.category).order_by('name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = self.category
        return ctx
