from django.contrib import admin
from .models import MedicineCategory, Medicine, PharmacyStock


@admin.register(MedicineCategory)
class MedicineCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'icon')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class PharmacyStockInline(admin.TabularInline):
    model = PharmacyStock
    extra = 1
    fields = ('pharmacy', 'price', 'quantity', 'is_available', 'expiry_date')
    autocomplete_fields = ['pharmacy']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'generic_name', 'category', 'dosage_form',
        'dosage', 'manufacturer', 'prescription_required'
    )
    list_filter = ('category', 'dosage_form', 'prescription_required', 'country')
    search_fields = ('name', 'generic_name', 'manufacturer', 'barcode')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PharmacyStockInline]

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'generic_name', 'slug', 'category', 'image')
        }),
        ('Tavsif', {
            'fields': ('description', 'indications', 'contraindications')
        }),
        ('Texnik xususiyatlar', {
            'fields': ('dosage_form', 'dosage', 'prescription_required', 'barcode')
        }),
        ('Ishlab chiqaruvchi', {
            'fields': ('manufacturer', 'country')
        }),
    )


@admin.register(PharmacyStock)
class PharmacyStockAdmin(admin.ModelAdmin):
    list_display = (
        'medicine', 'pharmacy', 'price', 'quantity',
        'is_available', 'last_updated'
    )
    list_filter = ('is_available', 'pharmacy__region', 'medicine__category')
    search_fields = ('medicine__name', 'pharmacy__name')
    list_editable = ('price', 'quantity', 'is_available')
    autocomplete_fields = ['medicine', 'pharmacy']
    readonly_fields = ('last_updated', 'created_at')
