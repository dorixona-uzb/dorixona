"""
Surxondaryo viloyati uchun boshlang'ich ma'lumotlarni yuklash.
Foydalanish: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
import random

from apps.pharmacies.models import Region, Pharmacy
from apps.medicines.models import MedicineCategory, Medicine, PharmacyStock


# Surxondaryo viloyati tumanlari va Termiz shahri
REGIONS_DATA = [
    {"name": "Termiz shahri", "slug": "termiz-shahri", "type": "city",
     "lat": 37.2242, "lng": 67.2783, "population": 182800,
     "description": "Surxondaryo viloyatining ma'muriy markazi."},
    {"name": "Angor tumani", "slug": "angor", "type": "district",
     "lat": 37.4769, "lng": 67.0344, "population": 130000,
     "description": "Termizdan shimoli-g'arbda joylashgan tuman."},
    {"name": "Bandixon tumani", "slug": "bandixon", "type": "district",
     "lat": 38.0667, "lng": 67.5333, "population": 75000,
     "description": "Viloyatning shimoliy qismidagi tuman."},
    {"name": "Boysun tumani", "slug": "boysun", "type": "district",
     "lat": 38.2114, "lng": 67.1989, "population": 110000,
     "description": "Tog'li hudud, qadimiy madaniyat o'chog'i."},
    {"name": "Denov tumani", "slug": "denov", "type": "district",
     "lat": 38.2647, "lng": 67.8911, "population": 360000,
     "description": "Viloyatning eng yirik tumanlaridan biri."},
    {"name": "Jarqo'rg'on tumani", "slug": "jarqorgon", "type": "district",
     "lat": 37.5083, "lng": 67.4225, "population": 240000,
     "description": "Termiz yaqinidagi yirik tuman."},
    {"name": "Qiziriq tumani", "slug": "qiziriq", "type": "district",
     "lat": 37.5258, "lng": 67.0722, "population": 130000,
     "description": "Viloyatning g'arbiy qismida joylashgan."},
    {"name": "Qumqo'rg'on tumani", "slug": "qumqorgon", "type": "district",
     "lat": 37.7811, "lng": 67.5800, "population": 195000,
     "description": "Markaziy tumanlardan biri."},
    {"name": "Muzrabot tumani", "slug": "muzrabot", "type": "district",
     "lat": 37.4900, "lng": 66.7500, "population": 130000,
     "description": "Viloyatning g'arbiy chegarasidagi tuman."},
    {"name": "Oltinsoy tumani", "slug": "oltinsoy", "type": "district",
     "lat": 38.2333, "lng": 67.7500, "population": 145000,
     "description": "Tog' etagidagi tuman."},
    {"name": "Sariosiyo tumani", "slug": "sariosiyo", "type": "district",
     "lat": 38.4131, "lng": 67.9264, "population": 130000,
     "description": "Shimoliy chegaradagi tog'li tuman."},
    {"name": "Sherobod tumani", "slug": "sherobod", "type": "district",
     "lat": 37.6700, "lng": 67.0186, "population": 200000,
     "description": "G'arbiy tumanlardan biri."},
    {"name": "Sho'rchi tumani", "slug": "shorchi", "type": "district",
     "lat": 37.9911, "lng": 67.7894, "population": 230000,
     "description": "Markaziy yirik tumanlardan biri."},
    {"name": "Termiz tumani", "slug": "termiz-tumani", "type": "district",
     "lat": 37.3000, "lng": 67.3000, "population": 165000,
     "description": "Termiz shahri atrofidagi tuman."},
    {"name": "Uzun tumani", "slug": "uzun", "type": "district",
     "lat": 38.4633, "lng": 68.0517, "population": 145000,
     "description": "Viloyatning shimoliy-sharqida joylashgan."},
]


# Dorilar kategoriyalari
CATEGORIES_DATA = [
    {"name": "Og'riq qoldiruvchi", "slug": "ogriq-qoldiruvchi", "icon": "fa-pills"},
    {"name": "Antibiotiklar", "slug": "antibiotiklar", "icon": "fa-capsules"},
    {"name": "Vitaminlar", "slug": "vitaminlar", "icon": "fa-leaf"},
    {"name": "Yurak-qon tomir", "slug": "yurak-qon-tomir", "icon": "fa-heart"},
    {"name": "Oshqozon-ichak", "slug": "oshqozon-ichak", "icon": "fa-stethoscope"},
    {"name": "Sovuq-grippga qarshi", "slug": "sovuq-grippga-qarshi", "icon": "fa-temperature-high"},
    {"name": "Allergiyaga qarshi", "slug": "allergiyaga-qarshi", "icon": "fa-shield-virus"},
    {"name": "Bolalar dorilari", "slug": "bolalar-dorilari", "icon": "fa-baby"},
]


# Namuna dorilar
MEDICINES_DATA = [
    # Og'riq qoldiruvchi
    {"name": "Analgin", "generic": "Metamizol natriy", "cat": "ogriq-qoldiruvchi",
     "manuf": "Farm-Sintez", "country": "O'zbekiston", "form": "tablet", "dosage": "500 mg", "rx": False,
     "indications": "Bosh og'rig'i, tish og'rig'i, mushak og'rig'i."},
    {"name": "Paracetamol", "generic": "Paracetamol", "cat": "ogriq-qoldiruvchi",
     "manuf": "Yuksel Pharma", "country": "Turkiya", "form": "tablet", "dosage": "500 mg", "rx": False,
     "indications": "Harorat, bosh og'rig'i, sovuq alomatlari."},
    {"name": "Ibuprofen", "generic": "Ibuprofen", "cat": "ogriq-qoldiruvchi",
     "manuf": "Hemofarm", "country": "Serbiya", "form": "tablet", "dosage": "400 mg", "rx": False,
     "indications": "Yallig'lanish, og'riq, harorat."},
    {"name": "Nurofen", "generic": "Ibuprofen", "cat": "ogriq-qoldiruvchi",
     "manuf": "Reckitt Benckiser", "country": "Buyuk Britaniya", "form": "tablet", "dosage": "200 mg", "rx": False,
     "indications": "Tez ta'sir qiluvchi og'riq qoldiruvchi."},
    {"name": "Diclofenac", "generic": "Diklofenak", "cat": "ogriq-qoldiruvchi",
     "manuf": "Hemofarm", "country": "Serbiya", "form": "tablet", "dosage": "50 mg", "rx": True,
     "indications": "Bo'g'im va mushak og'riqlari."},

    # Antibiotiklar
    {"name": "Amoksitsillin", "generic": "Amoxicillin", "cat": "antibiotiklar",
     "manuf": "Sandoz", "country": "Shveytsariya", "form": "capsule", "dosage": "500 mg", "rx": True,
     "indications": "Bakterial infektsiyalarni davolashda."},
    {"name": "Azitromitsin", "generic": "Azithromycin", "cat": "antibiotiklar",
     "manuf": "Pliva", "country": "Xorvatiya", "form": "tablet", "dosage": "500 mg", "rx": True,
     "indications": "Nafas yo'llari va terining bakterial infektsiyalari."},
    {"name": "Sumamed", "generic": "Azithromycin", "cat": "antibiotiklar",
     "manuf": "Pliva", "country": "Xorvatiya", "form": "tablet", "dosage": "500 mg", "rx": True,
     "indications": "Keng spektrli antibiotik."},
    {"name": "Ceftriakson", "generic": "Ceftriaxone", "cat": "antibiotiklar",
     "manuf": "Lupin", "country": "Hindiston", "form": "injection", "dosage": "1 g", "rx": True,
     "indications": "Og'ir bakterial infektsiyalar."},
    {"name": "Ampitsillin", "generic": "Ampicillin", "cat": "antibiotiklar",
     "manuf": "Belmedpreparaty", "country": "Belarus", "form": "capsule", "dosage": "250 mg", "rx": True,
     "indications": "Nafas, peshob yo'llari infektsiyalari."},

    # Vitaminlar
    {"name": "Vitamin C", "generic": "Askorbin kislotasi", "cat": "vitaminlar",
     "manuf": "Marbiopharm", "country": "Rossiya", "form": "tablet", "dosage": "500 mg", "rx": False,
     "indications": "Immunitet kuchaytirish."},
    {"name": "Revit", "generic": "Multivitamin", "cat": "vitaminlar",
     "manuf": "Farmstandart", "country": "Rossiya", "form": "tablet", "dosage": "100 dona", "rx": False,
     "indications": "Vitaminlar majmuasi."},
    {"name": "Vitamin D3", "generic": "Xolekaltsiferol", "cat": "vitaminlar",
     "manuf": "Solgar", "country": "AQSh", "form": "drops", "dosage": "10 ml", "rx": False,
     "indications": "Suyak salomatligi, kaltsiy assimilyatsiyasi."},
    {"name": "Vitamin B kompleks", "generic": "B vitaminlari", "cat": "vitaminlar",
     "manuf": "Sopharma", "country": "Bolgariya", "form": "tablet", "dosage": "30 dona", "rx": False,
     "indications": "Asab tizimi, energiya almashinuvi."},
    {"name": "Magne B6", "generic": "Magniy + B6", "cat": "vitaminlar",
     "manuf": "Sanofi", "country": "Fransiya", "form": "tablet", "dosage": "50 dona", "rx": False,
     "indications": "Magniy yetishmovchiligi, stress."},

    # Yurak-qon tomir
    {"name": "Validol", "generic": "Levomenthol", "cat": "yurak-qon-tomir",
     "manuf": "Farmstandart", "country": "Rossiya", "form": "tablet", "dosage": "60 mg", "rx": False,
     "indications": "Yurak sohasidagi og'riq, stenokardiya."},
    {"name": "Aspirin Cardio", "generic": "Asetilsalitsil kislotasi", "cat": "yurak-qon-tomir",
     "manuf": "Bayer", "country": "Germaniya", "form": "tablet", "dosage": "100 mg", "rx": False,
     "indications": "Qon ivishini oldini olish."},
    {"name": "Konkor", "generic": "Bisoprolol", "cat": "yurak-qon-tomir",
     "manuf": "Merck", "country": "Germaniya", "form": "tablet", "dosage": "5 mg", "rx": True,
     "indications": "Yuqori qon bosimi, stenokardiya."},
    {"name": "Enalapril", "generic": "Enalapril", "cat": "yurak-qon-tomir",
     "manuf": "Hemofarm", "country": "Serbiya", "form": "tablet", "dosage": "10 mg", "rx": True,
     "indications": "Gipertoniya."},

    # Oshqozon-ichak
    {"name": "Mezim Forte", "generic": "Pankreatin", "cat": "oshqozon-ichak",
     "manuf": "Berlin-Chemie", "country": "Germaniya", "form": "tablet", "dosage": "20 dona", "rx": False,
     "indications": "Hazm yaxshilash."},
    {"name": "Omeprazol", "generic": "Omeprazol", "cat": "oshqozon-ichak",
     "manuf": "Sandoz", "country": "Shveytsariya", "form": "capsule", "dosage": "20 mg", "rx": False,
     "indications": "Oshqozon yarasi, kislotalik."},
    {"name": "Smekta", "generic": "Diosmektit", "cat": "oshqozon-ichak",
     "manuf": "Ipsen", "country": "Fransiya", "form": "powder", "dosage": "3 g", "rx": False,
     "indications": "Diareya, oshqozon kuyishi."},
    {"name": "Festal", "generic": "Pankreatin + Safro", "cat": "oshqozon-ichak",
     "manuf": "Sanofi", "country": "Hindiston", "form": "tablet", "dosage": "20 dona", "rx": False,
     "indications": "Hazm muammolari."},

    # Sovuq-grippga qarshi
    {"name": "Coldrex", "generic": "Paracetamol + boshqalar", "cat": "sovuq-grippga-qarshi",
     "manuf": "GSK", "country": "Buyuk Britaniya", "form": "powder", "dosage": "5 g", "rx": False,
     "indications": "Grippga qarshi kompleks dori."},
    {"name": "Theraflu", "generic": "Paracetamol + boshqalar", "cat": "sovuq-grippga-qarshi",
     "manuf": "Novartis", "country": "Shveytsariya", "form": "powder", "dosage": "11.5 g", "rx": False,
     "indications": "Grippe va sovuq alomatlariga qarshi."},
    {"name": "Aflubin", "generic": "Gomeopatik", "cat": "sovuq-grippga-qarshi",
     "manuf": "Bittner", "country": "Avstriya", "form": "drops", "dosage": "20 ml", "rx": False,
     "indications": "Profilaktika va davolash."},
    {"name": "Strepsils", "generic": "Amilmetakrezol", "cat": "sovuq-grippga-qarshi",
     "manuf": "Reckitt Benckiser", "country": "Buyuk Britaniya", "form": "tablet", "dosage": "24 dona", "rx": False,
     "indications": "Tomoq og'rig'iga qarshi."},

    # Allergiyaga qarshi
    {"name": "Suprastin", "generic": "Xloropiramin", "cat": "allergiyaga-qarshi",
     "manuf": "Egis", "country": "Vengriya", "form": "tablet", "dosage": "25 mg", "rx": False,
     "indications": "Allergik reaksiyalar."},
    {"name": "Loratadin", "generic": "Loratadin", "cat": "allergiyaga-qarshi",
     "manuf": "Hemofarm", "country": "Serbiya", "form": "tablet", "dosage": "10 mg", "rx": False,
     "indications": "Mavsumiy allergiya, qichish."},
    {"name": "Zyrtec", "generic": "Tsetirizin", "cat": "allergiyaga-qarshi",
     "manuf": "UCB", "country": "Belgiya", "form": "tablet", "dosage": "10 mg", "rx": False,
     "indications": "Allergik rinit, krapivnitsa."},

    # Bolalar
    {"name": "Nurofen Bolalar uchun", "generic": "Ibuprofen", "cat": "bolalar-dorilari",
     "manuf": "Reckitt Benckiser", "country": "Buyuk Britaniya", "form": "syrup", "dosage": "100 ml", "rx": False,
     "indications": "Bolalardagi harorat va og'riq."},
    {"name": "Panadol Baby", "generic": "Paracetamol", "cat": "bolalar-dorilari",
     "manuf": "GSK", "country": "Buyuk Britaniya", "form": "syrup", "dosage": "100 ml", "rx": False,
     "indications": "Bolalardagi harorat."},
    {"name": "Bifidumbakterin", "generic": "Bifidobakteriyalar", "cat": "bolalar-dorilari",
     "manuf": "Microgen", "country": "Rossiya", "form": "powder", "dosage": "10 dona", "rx": False,
     "indications": "Disbakterioz, immunitet."},
]


# Namuna dorixonalar nomlari
PHARMACY_NAMES = [
    "Salomat Dorixona", "Shifo Dorixonasi", "Sog'lom Hayot",
    "Markaziy Dorixona", "Madad Dorixona", "Hayot Dorixonasi",
    "Tabib Dorixona", "Mehr Dorixonasi", "Ifor Dorixona",
    "Apteka Plyus", "Farma Lux", "Eko Apteka",
    "Sharq Tabobat", "Oltin Shifo", "Marvarid Dorixona",
]


class Command(BaseCommand):
    help = "Surxondaryo viloyati uchun namuna ma'lumotlarini yuklash"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval mavjud ma'lumotlarni o'chirish")

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING("Mavjud ma'lumotlar o'chirilmoqda..."))
            PharmacyStock.objects.all().delete()
            Medicine.objects.all().delete()
            MedicineCategory.objects.all().delete()
            Pharmacy.objects.all().delete()
            Region.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Boshlandi: Surxondaryo ma'lumotlari yuklanmoqda...\n"))

        # 1) Hududlarni yaratish
        self.stdout.write("Hududlar yaratilmoqda...")
        regions = {}
        for r in REGIONS_DATA:
            region, created = Region.objects.get_or_create(
                slug=r['slug'],
                defaults={
                    'name': r['name'], 'region_type': r['type'],
                    'latitude': r['lat'], 'longitude': r['lng'],
                    'population': r['population'], 'description': r['description'],
                }
            )
            regions[r['slug']] = region
            if created:
                self.stdout.write(f"  ✓ {r['name']}")
        self.stdout.write(self.style.SUCCESS(f"Jami hududlar: {len(regions)}\n"))

        # 2) Kategoriyalar
        self.stdout.write("Kategoriyalar yaratilmoqda...")
        categories = {}
        for c in CATEGORIES_DATA:
            cat, created = MedicineCategory.objects.get_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'icon': c['icon']}
            )
            categories[c['slug']] = cat
            if created:
                self.stdout.write(f"  ✓ {c['name']}")
        self.stdout.write(self.style.SUCCESS(f"Jami kategoriyalar: {len(categories)}\n"))

        # 3) Dorilar
        self.stdout.write("Dorilar yaratilmoqda...")
        medicines = []
        for m in MEDICINES_DATA:
            slug = slugify(m['name'])
            medicine, created = Medicine.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': m['name'], 'generic_name': m['generic'],
                    'category': categories[m['cat']], 'manufacturer': m['manuf'],
                    'country': m['country'], 'dosage_form': m['form'],
                    'dosage': m['dosage'], 'prescription_required': m['rx'],
                    'indications': m['indications'],
                    'description': f"{m['name']} ({m['generic']}) — {m['manuf']} ishlab chiqaruvchi.",
                }
            )
            medicines.append(medicine)
            if created:
                self.stdout.write(f"  ✓ {m['name']}")
        self.stdout.write(self.style.SUCCESS(f"Jami dorilar: {len(medicines)}\n"))

        # 4) Dorixonalar (har bir hududda 3-4 ta)
        self.stdout.write("Dorixonalar yaratilmoqda...")
        pharmacies = []
        for slug, region in regions.items():
            count = 4 if region.region_type == 'city' else 3
            for i in range(count):
                # Tasodifiy ofset (tuman markazidan ~5km radiusda)
                lat_offset = (random.random() - 0.5) * 0.08
                lng_offset = (random.random() - 0.5) * 0.08

                name = f"{random.choice(PHARMACY_NAMES)} #{i+1}"
                pharm_slug = slugify(f"{slug}-{name}-{i}")

                pharm, created = Pharmacy.objects.get_or_create(
                    slug=pharm_slug,
                    defaults={
                        'name': name, 'region': region,
                        'address': f"{region.name}, {random.randint(1, 50)}-uy",
                        'latitude': region.latitude + lat_offset,
                        'longitude': region.longitude + lng_offset,
                        'phone': f"+99876{random.randint(1000000, 9999999)}",
                        'working_hours': random.choice([
                            "08:00 - 22:00", "09:00 - 21:00", "08:00 - 20:00", "24/7"
                        ]),
                        'is_24_hours': random.random() < 0.2,
                        'has_delivery': random.random() < 0.6,
                        'is_active': True,
                        'is_verified': random.random() < 0.7,
                        'rating': round(random.uniform(3.5, 5.0), 1),
                        'description': f"{region.name}dagi ishonchli dorixona.",
                    }
                )
                pharmacies.append(pharm)
        self.stdout.write(self.style.SUCCESS(f"Jami dorixonalar: {len(pharmacies)}\n"))

        # 5) Stock — har bir dorixonada tasodifiy 60-90% dorilar mavjud
        self.stdout.write("Dori zaxiralari yaratilmoqda...")
        stock_count = 0
        for pharm in pharmacies:
            # Dorilarning 60-90% mavjud
            available = random.sample(medicines, k=random.randint(int(len(medicines)*0.6), int(len(medicines)*0.9)))
            for med in available:
                # Bazaviy narx (kategoriyaga qarab)
                base_prices = {
                    'ogriq-qoldiruvchi': (5000, 25000),
                    'antibiotiklar': (15000, 80000),
                    'vitaminlar': (15000, 120000),
                    'yurak-qon-tomir': (10000, 90000),
                    'oshqozon-ichak': (8000, 60000),
                    'sovuq-grippga-qarshi': (10000, 50000),
                    'allergiyaga-qarshi': (12000, 45000),
                    'bolalar-dorilari': (15000, 70000),
                }
                pmin, pmax = base_prices.get(med.category.slug, (10000, 50000))
                # Dorixonalar orasida ±15% farq
                price = random.randint(pmin, pmax)
                price = int(price * random.uniform(0.85, 1.15))

                stock, created = PharmacyStock.objects.get_or_create(
                    pharmacy=pharm, medicine=med,
                    defaults={
                        'price': Decimal(price),
                        'quantity': random.randint(5, 200),
                        'is_available': True,
                    }
                )
                if created:
                    stock_count += 1
        self.stdout.write(self.style.SUCCESS(f"Jami zaxira yozuvlari: {stock_count}\n"))

        # 6) Demo admin foydalanuvchi
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', email='admin@dorixona.uz', password='admin123'
            )
            self.stdout.write(self.style.SUCCESS("Admin foydalanuvchi yaratildi:"))
            self.stdout.write("  Login: admin")
            self.stdout.write("  Parol: admin123\n")

        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(self.style.SUCCESS("✓ Barcha ma'lumotlar muvaffaqiyatli yuklandi!"))
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(f"\nJami:")
        self.stdout.write(f"  Hududlar: {Region.objects.count()}")
        self.stdout.write(f"  Kategoriyalar: {MedicineCategory.objects.count()}")
        self.stdout.write(f"  Dorilar: {Medicine.objects.count()}")
        self.stdout.write(f"  Dorixonalar: {Pharmacy.objects.count()}")
        self.stdout.write(f"  Stock yozuvlari: {PharmacyStock.objects.count()}")
        self.stdout.write("\nServerni ishga tushirish: python manage.py runserver\n")
