# 💊 Surxondaryo Dorixona — Onlayn dorixona qidiruv tizimi

Surxondaryo viloyati barcha tumanlari va Termiz shahri bo'yicha **eng yaqin dorixonalarni topish, dori narxlarini taqqoslash va mavjudligini tekshirish** uchun Django asosidagi to'liq web ilova.

## 🌟 Asosiy imkoniyatlar

- 🗺️ **Interaktiv xarita** — Leaflet asosidagi xarita orqali dorixonalarni ko'rish
- 📍 **Geolokatsiya** — Brauzer orqali eng yaqin dorixonani aniqlash
- 💰 **Narxlarni taqqoslash** — Bir xil dorining barcha dorixonalardagi narxini ko'rish
- 🔍 **Kuchli qidiruv** — Dori nomi, INN, ishlab chiqaruvchi bo'yicha qidirish
- 🏥 **Dorixona profili** — Manzil, ish vaqti, telefon, yetkazib berish ma'lumotlari
- 👨‍⚕️ **Dorixona egasi paneli** — Stockni boshqarish, narxlarni yangilash
- 🌐 **API** — Avtokomplit, yaqin dorixonalar, mavjudlik tekshirish

## 🏗️ Texnologiyalar

- **Backend:** Django 5.x, Django REST Framework
- **Frontend:** Bootstrap 5, FontAwesome, Leaflet.js
- **Ma'lumotlar bazasi:** SQLite (default), PostgreSQL (ishlab chiqarish)
- **Til:** O'zbek (asosiy), rus, ingliz tayyor

## 📂 Hududlar (15 ta)

Termiz shahri va 14 ta tuman: Angor, Bandixon, Boysun, Denov, Jarqo'rg'on, Qiziriq, Qumqo'rg'on, Muzrabot, Oltinsoy, Sariosiyo, Sherobod, Sho'rchi, Termiz tumani, Uzun.

## 🚀 O'rnatish va ishga tushirish

### 1) Loyihani yuklab oling

```bash
cd surxondaryo_dorixona
```

### 2) Virtual muhit yarating

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
# yoki Windows uchun:
venv\Scripts\activate
```

### 3) Kerakli kutubxonalarni o'rnating

```bash
pip install -r requirements.txt
```

### 4) Atrof-muhit fayli (.env)

```bash
cp .env.example .env
# .env faylini tahrirlang (SECRET_KEY ni o'zgartiring)
```

### 5) Migratsiyalarni qo'llang

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6) Boshlang'ich ma'lumotlarni yuklang

```bash
python manage.py seed_data
```

Bu buyruq:
- 15 ta hudud (Termiz + 14 tuman)
- 8 ta kategoriya
- 30+ ta dori
- ~46 ta dorixona
- ~1000+ ta narx yozuvi
- Admin foydalanuvchi (`admin` / `admin123`)

ni yaratadi.

### 7) Statik fayllarni yig'ing (production uchun)

```bash
python manage.py collectstatic --noinput
```

### 8) Serverni ishga tushiring

```bash
python manage.py runserver
```

Brauzeringizda oching: **http://127.0.0.1:8000/**

Admin paneli: **http://127.0.0.1:8000/admin/** (login: `admin`, parol: `admin123`)

## 📁 Loyiha tuzilishi

```
surxondaryo_dorixona/
├── config/                     # Django sozlamalari
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                       # Ilovalar
│   ├── pharmacies/             # Dorixonalar va hududlar
│   ├── medicines/              # Dorilar va kategoriyalar
│   ├── search/                 # Qidiruv funksiyasi
│   ├── accounts/               # Foydalanuvchilar
│   └── api/                    # JSON API
├── templates/                  # HTML shablonlar
├── static/                     # CSS, JS, rasmlar
├── media/                      # Yuklangan rasmlar
├── manage.py
├── requirements.txt
└── README.md
```

## 🌐 Asosiy URL'lar

| Manzil | Tavsif |
|--------|--------|
| `/` | Bosh sahifa, xarita va statistika |
| `/pharmacies/` | Barcha dorixonalar ro'yxati |
| `/pharmacy/<slug>/` | Dorixona batafsil sahifasi |
| `/region/<slug>/` | Tuman bo'yicha dorixonalar |
| `/medicine/` | Barcha dorilar |
| `/medicine/<slug>/` | Dori batafsil sahifasi |
| `/search/results/` | Qidiruv natijalari |
| `/accounts/login/` | Tizimga kirish |
| `/accounts/dashboard/` | Foydalanuvchi paneli |
| `/admin/` | Boshqaruv paneli |

## 🔌 API endpointlari

| Endpoint | Tavsif |
|----------|--------|
| `GET /api/autocomplete/?q=<so'rov>` | Avtomatik to'ldirish |
| `GET /api/nearby/?lat=&lng=&radius=` | Yaqin dorixonalar |
| `GET /api/medicine/<id>/availability/` | Dori mavjudligi |
| `GET /api/regions/` | Hududlar ro'yxati |

## 🛠️ Production deploy

### PostgreSQL bilan

`.env` faylida:
```
DEBUG=False
DATABASE_URL=postgres://user:password@host:5432/dbname
ALLOWED_HOSTS=yourdomain.com
```

### Gunicorn bilan ishga tushirish

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 📝 Litsenziya

MIT — erkin foydalaning.

## 💡 Eslatma

Bu MVP versiya bo'lib, demo ma'lumotlar bilan jihozlangan. Real loyiha uchun:
- Real dorixona ma'lumotlarini yuklang
- To'lov tizimi (Click, Payme) integratsiya qiling
- SMS xabarnomalar qo'shing
- Mobil ilova uchun API kengaytiring

---

**Mualliflik:** Surxondaryo Dorixona jamoasi
