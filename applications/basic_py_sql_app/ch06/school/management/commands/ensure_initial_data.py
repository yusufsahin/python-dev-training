from django.core.management.base import BaseCommand

from school.models import Department
from school.seed import seed_demo_data


class Command(BaseCommand):
    help = "Veritabanında hiç bölüm yoksa demo seed çalıştırır (konteyner ilk açılış)."

    def handle(self, *args, **options):
        if Department.objects.exists():
            self.stdout.write(self.style.WARNING("Seed skipped: database already has departments."))
            return
        self.stdout.write("Running initial seed…")
        seed_demo_data(self.stdout)
        self.stdout.write(self.style.SUCCESS("Initial data ready."))
