"""
JSON API endpointlar — frontend AJAX uchun.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from apps.pharmacies.models import Pharmacy, Region
from apps.medicines.models import Medicine, PharmacyStock


@require_GET
def search_autocomplete(request):
    """Qidiruv satri uchun autocomplete API."""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    medicines = Medicine.objects.filter(
        Q(name__icontains=query) | Q(generic_name__icontains=query)
    )[:10]

    results = [
        {
            'id': m.id,
            'name': m.name,
            'dosage': m.dosage,
            'generic_name': m.generic_name,
            'url': m.get_absolute_url(),
            'available_count': m.available_pharmacies_count,
        }
        for m in medicines
    ]
    return JsonResponse({'results': results})


@require_GET
def nearby_pharmacies(request):
    """Eng yaqin dorixonalarni topish (foydalanuvchi koordinatasi bo'yicha)."""
    try:
        lat = float(request.GET.get('lat'))
        lng = float(request.GET.get('lng'))
    except (ValueError, TypeError):
        return JsonResponse({'error': 'lat va lng parametrlari talab qilinadi'}, status=400)

    radius = float(request.GET.get('radius', 50))  # km da
    limit = int(request.GET.get('limit', 20))

    pharmacies = Pharmacy.objects.filter(is_active=True).select_related('region')

    results = []
    for p in pharmacies:
        distance = p.distance_to(lat, lng)
        if distance <= radius:
            results.append({
                'id': p.id,
                'name': p.name,
                'region': p.region.name,
                'address': p.address,
                'phone': p.phone,
                'lat': p.latitude,
                'lng': p.longitude,
                'distance_km': distance,
                'is_24h': p.is_24_hours,
                'has_delivery': p.has_delivery,
                'url': p.get_absolute_url(),
            })

    results.sort(key=lambda x: x['distance_km'])
    return JsonResponse({
        'results': results[:limit],
        'count': len(results),
    })


@require_GET
def medicine_availability(request, medicine_id):
    """Berilgan dori qaysi dorixonalarda mavjudligini ko'rsatadi."""
    try:
        medicine = Medicine.objects.get(id=medicine_id)
    except Medicine.DoesNotExist:
        return JsonResponse({'error': 'Dori topilmadi'}, status=404)

    region_slug = request.GET.get('region')
    stock_qs = medicine.stock_entries.filter(
        is_available=True, quantity__gt=0
    ).select_related('pharmacy', 'pharmacy__region')

    if region_slug:
        stock_qs = stock_qs.filter(pharmacy__region__slug=region_slug)

    results = [
        {
            'pharmacy_id': s.pharmacy.id,
            'pharmacy_name': s.pharmacy.name,
            'region': s.pharmacy.region.name,
            'address': s.pharmacy.address,
            'phone': s.pharmacy.phone,
            'price': float(s.price),
            'quantity': s.quantity,
            'lat': s.pharmacy.latitude,
            'lng': s.pharmacy.longitude,
            'is_24h': s.pharmacy.is_24_hours,
            'pharmacy_url': s.pharmacy.get_absolute_url(),
        }
        for s in stock_qs.order_by('price')
    ]

    return JsonResponse({
        'medicine': {
            'name': medicine.name,
            'generic_name': medicine.generic_name,
            'dosage': medicine.dosage,
        },
        'available_at': results,
        'total': len(results),
    })


@require_GET
def regions_list(request):
    """Barcha tumanlar ro'yxati JSON formatda."""
    regions = Region.objects.all().order_by('name')
    return JsonResponse({
        'regions': [
            {
                'id': r.id,
                'name': r.name,
                'slug': r.slug,
                'lat': r.latitude,
                'lng': r.longitude,
                'pharmacy_count': r.pharmacy_count,
            }
            for r in regions
        ]
    })
