from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalog.models import Category, Product


SEED_CATEGORIES = [
    {
        "name": "Elektronik",
        "slug": "elektronik",
        "description": "Bilgisayar, ses ve mobil aksesuarlar.",
        "parent_slug": None,
    },
    {
        "name": "Bilgisayar Aksesuarları",
        "slug": "bilgisayar-aksesuarlari",
        "description": "Klavye, mouse, kablolar.",
        "parent_slug": "elektronik",
    },
    {
        "name": "Ev ve Yaşam",
        "slug": "ev-yasam",
        "description": "Mutfak, dekorasyon ve günlük kullanım.",
        "parent_slug": None,
    },
    {
        "name": "Kitap",
        "slug": "kitap",
        "description": "Roman, teknik ve çocuk kitapları.",
        "parent_slug": None,
    },
]

SEED_PRODUCTS = [
    {
        "category_slug": "elektronik",
        "name": "Kablosuz Kulaklık Pro",
        "slug": "kablosuz-kulaklik-pro",
        "description": "Gürültü önleyici, 30 saat pil ömrü.",
        "price": Decimal("1299.90"),
        "stock": 25,
    },
    {
        "category_slug": "elektronik",
        "name": "Taşınabilir Bluetooth Hoparlör",
        "slug": "tasinabilir-bluetooth-hoparlor",
        "description": "IPX7 su geçirmez, kompakt tasarım.",
        "price": Decimal("549.00"),
        "stock": 40,
    },
    {
        "category_slug": "bilgisayar-aksesuarlari",
        "name": "Mekanik Klavye RGB",
        "slug": "mekanik-klavye-rgb",
        "description": "Hot-swap anahtarlar, Türkçe Q düzeni.",
        "price": Decimal("1899.00"),
        "stock": 15,
    },
    {
        "category_slug": "bilgisayar-aksesuarlari",
        "name": "USB-C Hub 7 in 1",
        "slug": "usb-c-hub-7-in-1",
        "description": "HDMI, USB-A, SD ve güç dağıtımı.",
        "price": Decimal("449.50"),
        "stock": 60,
    },
    {
        "category_slug": "ev-yasam",
        "name": "Kahve Fincanı Seti",
        "slug": "kahve-fincani-seti",
        "description": "Porselen 2 kişilik set.",
        "price": Decimal("149.90"),
        "stock": 100,
    },
    {
        "category_slug": "ev-yasam",
        "name": "Bambu Kesme Tahtası",
        "slug": "bambu-kesme-tahtasi",
        "description": "Doğal bambu, 35x25 cm.",
        "price": Decimal("89.00"),
        "stock": 0,
    },
    {
        "category_slug": "kitap",
        "name": "Python ile Veri Analizi",
        "slug": "python-ile-veri-analizi",
        "description": "Pandas ve NumPy ile pratik örnekler.",
        "price": Decimal("312.00"),
        "stock": 20,
    },
    {
        "category_slug": "kitap",
        "name": "Django Web Geliştirme",
        "slug": "django-web-gelistirme",
        "description": "Monolit uygulamalardan API’lere.",
        "price": Decimal("275.00"),
        "stock": 12,
    },
]


class Command(BaseCommand):
    help = "Load sample categories and products (idempotent get_or_create)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-demo-user",
            action="store_true",
            help="Create user 'demo' / storium-demo-2024 for checkout tests (dev only).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        slug_to_category: dict[str, Category] = {}

        for row in SEED_CATEGORIES:
            parent = None
            if row["parent_slug"]:
                parent = slug_to_category.get(row["parent_slug"])
                if parent is None:
                    parent = Category.objects.filter(slug=row["parent_slug"]).first()
            cat, created = Category.objects.get_or_create(
                slug=row["slug"],
                defaults={
                    "name": row["name"],
                    "description": row["description"],
                    "parent": parent,
                    "is_active": True,
                },
            )
            if not created:
                cat.name = row["name"]
                cat.description = row["description"]
                cat.parent = parent
                cat.is_active = True
                cat.save()
            slug_to_category[row["slug"]] = cat
            action = "created" if created else "updated"
            self.stdout.write(f"  category [{action}] {cat.slug}")

        for row in SEED_PRODUCTS:
            cat = slug_to_category.get(row["category_slug"])
            if cat is None:
                cat = Category.objects.get(slug=row["category_slug"])
            obj, created = Product.objects.get_or_create(
                slug=row["slug"],
                defaults={
                    "category": cat,
                    "name": row["name"],
                    "description": row["description"],
                    "price": row["price"],
                    "stock": row["stock"],
                    "is_active": True,
                },
            )
            if not created:
                obj.category = cat
                obj.name = row["name"]
                obj.description = row["description"]
                obj.price = row["price"]
                obj.stock = row["stock"]
                obj.is_active = True
                obj.save()
            action = "created" if created else "updated"
            self.stdout.write(f"  product [{action}] {obj.slug}")

        if options["with_demo_user"]:
            u, created = User.objects.get_or_create(
                username="demo",
                defaults={"email": "demo@storium.local"},
            )
            u.set_password("storium-demo-2024")
            u.save()
            self.stdout.write(
                self.style.WARNING(
                    "  demo user: username=demo password=storium-demo-2024 (dev only)",
                ),
            )

        self.stdout.write(self.style.SUCCESS("Seed finished."))
