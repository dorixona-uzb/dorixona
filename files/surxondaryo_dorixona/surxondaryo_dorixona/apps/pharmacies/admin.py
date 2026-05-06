from django.contrib import admin
from django.utils.html import format_html
from .models import Region, Pharmacy


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'region_type', 'population', 'pharmacy_count', 'latitude', 'longitude')
    list_filter = ('region_type',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'region', 'phone', 'is_24_hours',
        'has_delivery', 'is_verified', 'is_active', 'rating'
    )
    list_filter = ('region', 'is_24_hours', 'has_delivery', 'is_verified', 'is_active')
    search_fields = ('name', 'address', 'phone')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_verified', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'map_link')

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug', 'region', 'description')
        }),
        ('Joylashuv', {
            'fields': ('address', 'latitude', 'longitude', 'map_link')
        }),
        ('Aloqa', {
            'fields': ('phone', 'phone_secondary')
        }),
        ('Ish tartibi', {
            'fields': ('working_hours', 'is_24_hours', 'has_delivery')
        }),
        ('Boshqaruv', {
            'fields': ('owner', 'is_active', 'is_verified', 'rating')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def map_link(self, obj):
        if obj.latitude and obj.longitude:
            url = obj.google_maps_url
            return format_html('<a href="{}" target="_blank">Google Mapsda ko\'rish</a>', url)
        return "—"
    map_link.short_description = "Xaritada ko'rish"
