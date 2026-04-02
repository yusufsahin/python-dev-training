from django.core.management.base import BaseCommand

from school.seed import seed_demo_data


class Command(BaseCommand):
    help = "Creates sample departments and students (skips duplicates via services)."

    def handle(self, *args, **options):
        seed_demo_data(self.stdout)
