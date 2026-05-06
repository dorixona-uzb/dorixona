"""Qidiruv tarixini saqlash uchun model."""
from django.db import models
from django.contrib.auth.models import User


class SearchHistory(models.Model):
    """Statistika va analitika uchun qidiruv tarixi."""
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='searches', verbose_name='Foydalanuvchi'
    )
    query = models.CharField('Qidiruv so\'rovi', max_length=300)
    region = models.ForeignKey(
        'pharmacies.Region', null=True, blank=True,
        on_delete=models.SET_NULL, verbose_name='Hudud'
    )
    results_count = models.PositiveIntegerField('Topilgan natijalar', default=0)
    user_lat = models.FloatField('Foydalanuvchi kengligi', null=True, blank=True)
    user_lng = models.FloatField('Foydalanuvchi uzunligi', null=True, blank=True)
    ip_address = models.GenericIPAddressField('IP', null=True, blank=True)
    user_agent = models.CharField('User-Agent', max_length=300, blank=True)
    searched_at = models.DateTimeField('Qidirilgan vaqt', auto_now_add=True)

    class Meta:
        verbose_name = 'Qidiruv tarixi'
        verbose_name_plural = 'Qidiruv tarixi'
        ordering = ['-searched_at']
        indexes = [models.Index(fields=['query', '-searched_at'])]

    def __str__(self):
        return f"{self.query} ({self.searched_at:%Y-%m-%d %H:%M})"
