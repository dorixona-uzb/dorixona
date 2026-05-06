"""
Surxondaryo Dorixona — Dori-darmon modellari
"""
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class MedicineCategory(models.Model):
    """Dorilar turkumi (antibiotik, vitamin, og'riq qoldiruvchi va h.k.)."""
    name = models.CharField('Nomi', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=120, unique=True, blank=True)
    description = models.TextField('Tavsif', blank=True)
    icon = models.CharField(
        'Icon (FontAwesome class)', max_length=50, blank=True,
        default='fa-pills'
    )
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='children', verbose_name='Asosiy turkum'
    )

    class Meta:
        verbose_name = 'Dori turkumi'
        verbose_name_plural = 'Dori turkumlari'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=False)
        super().save(*args, **kwargs)


class Medicine(models.Model):
    """Dori-darmon."""
    DOSAGE_FORM_CHOICES = [
        ('tablet', 'Tabletka'),
        ('capsule', 'Kapsula'),
        ('syrup', 'Sirop'),
        ('injection', 'Inyeksiya / Ampula'),
        ('cream', 'Krem / Maz'),
        ('drops', 'Tomchi'),
        ('powder', 'Kukun'),
        ('spray', 'Sprey'),
        ('other', 'Boshqa'),
    ]

    name = models.CharField('Tijorat nomi', max_length=200)
    generic_name = models.CharField('Xalqaro nomi (INN)', max_length=200, blank=True)
    slug = models.SlugField('Slug', max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        MedicineCategory, on_delete=models.SET_NULL, null=True,
        related_name='medicines', verbose_name='Turkum'
    )
    manufacturer = models.CharField(
        'Ishlab chiqaruvchi', max_length=200, blank=True
    )
    country = models.CharField('Mamlakat', max_length=100, blank=True)
    description = models.TextField('Tavsif', blank=True)
    indications = models.TextField('Foydalanish ko\'rsatmalari', blank=True)
    contraindications = models.TextField('Qarshi ko\'rsatmalar', blank=True)
    dosage_form = models.CharField(
        'Shakli', max_length=20, choices=DOSAGE_FORM_CHOICES, default='tablet'
    )
    dosage = models.CharField(
        'Dozasi', max_length=100, blank=True,
        help_text='Masalan: 500 mg, 100 ml'
    )
    prescription_required = models.BooleanField(
        'Retsept talab qilinadi', default=False
    )
    image = models.ImageField(
        'Rasm', upload_to='medicines/', blank=True, null=True
    )
    barcode = models.CharField(
        'Shtrix-kod', max_length=20, blank=True, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dori'
        verbose_name_plural = 'Dorilar'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['generic_name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.dosage})" if self.dosage else self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.name}-{self.dosage}", allow_unicode=False)
            self.slug = base or slugify(self.name)
            counter = 1
            while Medicine.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('medicines:detail', kwargs={'slug': self.slug})

    @property
    def available_pharmacies_count(self):
        return self.stock_entries.filter(
            is_available=True, quantity__gt=0
        ).count()

    @property
    def min_price(self):
        return self.stock_entries.filter(
            is_available=True, quantity__gt=0
        ).order_by('price').first()

    @property
    def max_price(self):
        return self.stock_entries.filter(
            is_available=True, quantity__gt=0
        ).order_by('-price').first()


class PharmacyStock(models.Model):
    """Dorixonadagi dori zaxirasi va narxi."""
    pharmacy = models.ForeignKey(
        'pharmacies.Pharmacy', on_delete=models.CASCADE,
        related_name='stock_items', verbose_name='Dorixona'
    )
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE,
        related_name='stock_entries', verbose_name='Dori'
    )
    price = models.DecimalField(
        'Narx (so\'m)', max_digits=12, decimal_places=2
    )
    quantity = models.PositiveIntegerField('Miqdori', default=0)
    is_available = models.BooleanField('Mavjud', default=True)
    expiry_date = models.DateField(
        'Yaroqlilik muddati', null=True, blank=True
    )
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Dorixona zaxirasi'
        verbose_name_plural = 'Dorixona zaxiralari'
        unique_together = [('pharmacy', 'medicine')]
        ordering = ['-last_updated']
        indexes = [
            models.Index(fields=['pharmacy', 'is_available']),
            models.Index(fields=['medicine', 'is_available']),
        ]

    def __str__(self):
        return f"{self.medicine.name} — {self.pharmacy.name} ({self.price} so'm)"

    @property
    def is_in_stock(self):
        return self.is_available and self.quantity > 0
