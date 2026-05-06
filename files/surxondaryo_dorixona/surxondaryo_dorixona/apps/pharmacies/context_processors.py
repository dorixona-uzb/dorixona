"""Context processorlar — har bir templateda mavjud bo'ladi."""
from .models import Region


def regions_processor(request):
    """Barcha tumanlarni har bir templatega yetkazadi (navbar uchun)."""
    return {
        'all_regions': Region.objects.all().order_by('name'),
    }
