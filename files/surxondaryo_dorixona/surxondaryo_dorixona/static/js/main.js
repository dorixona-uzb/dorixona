/**
 * Surxondaryo Dorixona — Asosiy JavaScript
 */

// Geolocation yordamchisi
const Geolocation = {
    get: function(callback, errorCallback) {
        if (!navigator.geolocation) {
            alert("Brauzeringiz joylashuvni aniqlashni qo'llab-quvvatlamaydi.");
            return;
        }
        navigator.geolocation.getCurrentPosition(
            (position) => {
                callback({
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                    accuracy: position.coords.accuracy
                });
            },
            (error) => {
                console.error("Joylashuvni aniqlashda xato:", error);
                if (errorCallback) errorCallback(error);
                else alert("Joylashuvni aniqlab bo'lmadi. Iltimos, ruxsat bering.");
            },
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
        );
    }
};

// Locate tugmalari uchun universal handler
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-locate]').forEach(btn => {
        btn.addEventListener('click', function() {
            const targetLat = document.querySelector(this.dataset.locate + '-lat') ||
                              document.getElementById('user-lat');
            const targetLng = document.querySelector(this.dataset.locate + '-lng') ||
                              document.getElementById('user-lng');

            const original = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            this.disabled = true;

            Geolocation.get((coords) => {
                if (targetLat) targetLat.value = coords.lat;
                if (targetLng) targetLng.value = coords.lng;
                this.innerHTML = '<i class="fas fa-check text-success"></i> Aniqlandi';
                setTimeout(() => {
                    this.innerHTML = original;
                    this.disabled = false;
                }, 2000);
            }, () => {
                this.innerHTML = original;
                this.disabled = false;
            });
        });
    });

    // Avtomatik to'ldirish (autocomplete)
    const searchInput = document.getElementById('global-search');
    const suggestionsBox = document.getElementById('search-suggestions');

    if (searchInput && suggestionsBox) {
        let timer;
        searchInput.addEventListener('input', function() {
            clearTimeout(timer);
            const query = this.value.trim();
            if (query.length < 2) {
                suggestionsBox.style.display = 'none';
                return;
            }
            timer = setTimeout(() => {
                fetch(`/api/autocomplete/?q=${encodeURIComponent(query)}`)
                    .then(res => res.json())
                    .then(data => {
                        if (!data.results || data.results.length === 0) {
                            suggestionsBox.style.display = 'none';
                            return;
                        }
                        suggestionsBox.innerHTML = data.results.map(item =>
                            `<a href="/medicine/${item.slug}/" class="suggestion-item">
                                <i class="fas fa-pills me-2 text-primary"></i>
                                <span class="suggestion-name">${item.name}</span>
                                ${item.generic_name ? `<small class="text-muted ms-2">${item.generic_name}</small>` : ''}
                            </a>`
                        ).join('');
                        suggestionsBox.style.display = 'block';
                    })
                    .catch(err => console.error(err));
            }, 250);
        });

        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
                suggestionsBox.style.display = 'none';
            }
        });
    }
});

// Telefon raqamini formatlash
function formatPhone(phone) {
    return phone.replace(/(\+998)(\d{2})(\d{3})(\d{2})(\d{2})/, '$1 ($2) $3-$4-$5');
}

// Narxni formatlash
function formatPrice(price) {
    return new Intl.NumberFormat('uz-UZ').format(price) + " so'm";
}

// Masofani formatlash
function formatDistance(km) {
    if (km < 1) return Math.round(km * 1000) + " m";
    return km.toFixed(1) + " km";
}
