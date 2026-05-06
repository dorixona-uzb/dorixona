"""Foydalanuvchi profili."""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Standart User modeliga qo'shimcha ma'lumotlar."""
    USER_TYPE_CHOICES = [
        ('customer', 'Mijoz'),
        ('pharmacy_owner', 'Dorixona egasi'),
        ('admin', 'Administrator'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='profile', verbose_name='Foydalanuvchi'
    )
    user_type = models.CharField(
        'Turi', max_length=20, choices=USER_TYPE_CHOICES, default='customer'
    )
    phone = models.CharField('Telefon', max_length=20, blank=True)
    region = models.ForeignKey(
        'pharmacies.Region', null=True, blank=True,
        on_delete=models.SET_NULL, verbose_name='Hudud'
    )
    avatar = models.ImageField('Avatar', upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foydalanuvchi profili'
        verbose_name_plural = 'Foydalanuvchi profillari'

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"
