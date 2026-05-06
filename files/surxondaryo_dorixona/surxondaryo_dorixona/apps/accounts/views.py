"""Foydalanuvchi autentifikatsiya va dashboard."""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django import forms

from apps.pharmacies.models import Pharmacy
from apps.medicines.models import Medicine, PharmacyStock


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=False, label='Ism')
    last_name = forms.CharField(max_length=30, required=False, label='Familiya')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('accounts:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            next_url = request.GET.get('next', 'accounts:dashboard')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Muvaffaqiyatli chiqdingiz.")
    return redirect('pharmacies:home')


@login_required
def dashboard_view(request):
    """Dorixona egasi yoki oddiy foydalanuvchi paneli."""
    user = request.user
    pharmacies = Pharmacy.objects.filter(owner=user).select_related('region')

    context = {
        'pharmacies': pharmacies,
        'has_pharmacies': pharmacies.exists(),
    }

    if pharmacies.exists():
        # Dorixona egasi uchun statistika
        total_stock = PharmacyStock.objects.filter(
            pharmacy__in=pharmacies
        ).count()
        available_stock = PharmacyStock.objects.filter(
            pharmacy__in=pharmacies, is_available=True, quantity__gt=0
        ).count()

        context.update({
            'total_stock': total_stock,
            'available_stock': available_stock,
            'total_pharmacies': pharmacies.count(),
        })

    return render(request, 'accounts/dashboard.html', context)
