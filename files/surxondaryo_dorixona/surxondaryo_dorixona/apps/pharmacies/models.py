"""
Surxondaryo Dorixona — Asosiy modellar
"""
from math import radians, sin, cos, sqrt, atan2
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Region(models.Model):
    """Surxondaryo viloyatining tumanlari va shahri."""
    REGION_TYPE_CHOICES = [
        ('city', 'Shahar'),
        ('district', 'Tuman'),
    ]

    name = models.CharField('Nomi', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=120, unique=True, blank=True)
    region_type = models.CharField(
        'Turi', max_length=10, choices=REGION_TYPE_CHOICES, default='district'
    )
    latitude = models.FloatField('Kenglik (latitude)')
    longitude = models.FloatField('Uzunlik (longitude)')
    population = models.PositiveIntegerField('Aholi soni', null=True, blank=True)
    description = models.TextField('Tavsif', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Hudud'
        verbose_name_plural = 'Hududlar (tumanlar)'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pharmacies:region_detail', kwargs={'slug': self.slug})

    @property
    def pharmacy_count(self):
        return self.pharmacies.filter(is_active=True).count()


class Pharmacy(models.Model):
    """Dorixona modeli."""
    name = models.CharField('Dorixona nomi', max_length=200)
    slug = models.SlugField('Slug', max_length=220, unique=True, blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE,
        related_name='pharmacies', verbose_name='Hudud'
    )
    address = models.CharField('Manzil', max_length=300)
    latitude = models.FloatField('Kenglik')
    longitude = models.FloatField('Uzunlik')
    phone = models.CharField('Telefon', max_length=20)
    phone_secondary = models.CharField(
        'Qo\'shimcha telefon', max_length=20, blank=True
    )
    working_hours = models.CharField(
        'Ish vaqti', max_length=100, default='09:00 - 21:00'
    )
    is_24_hours = models.BooleanField('24/7 ishlaydi', default=False)
    has_delivery = models.BooleanField('Yetkazib berish bor', default=False)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='pharmacies', verbose_name='Egasi'
    )
    description = models.TextField('Tavsif', blank=True)
    is_active = models.BooleanField('Faol', default=True)
    is_verified = models.BooleanField('Tasdiqlangan', default=False)
    rating = models.DecimalField(
        'Reyting', max_digits=3, decimal_places=2, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dorixona'
        verbose_name_plural = 'Dorixonalar'
        ordering = ['-is_verified', 'name']
        indexes = [
            models.Index(fields=['region', 'is_active']),
            models.Index(fields=['latitude', 'longitude']),
        ]

    def __str__(self):
        return f"{self.name} — {self.region.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.region.name}", allow_unicode=False)
            self.slug = base_slug
            counter = 1
            while Pharmacy.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pharmacies:detail', kwargs={'slug': self.slug})

    def distance_to(self, lat, lng):
        """Haversine formulasi yordamida masofani km da hisoblaydi."""
        R = 6371  # Yer radiusi km
        dlat = radians(lat - self.latitude)
        dlon = radians(lng - self.longitude)
        a = (sin(dlat / 2) ** 2 +
             cos(radians(self.latitude)) * cos(radians(lat)) *
             sin(dlon / 2) ** 2)
        return round(R * 2 * atan2(sqrt(a), sqrt(1 - a)), 2)

    @property
    def medicine_count(self):
        return self.stock_items.filter(is_available=True).count()

    @property
    def google_maps_url(self):
        return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"

    @property
    def yandex_maps_url(self):
        return f"https://yandex.com/maps/?pt={self.longitude},{self.latitude}&z=17"
