from django.core.management.base import BaseCommand

from greeva.hydroponics.integrations.nbri_fetch import sync_nbri_records


class Command(BaseCommand):
    help = "Sync NBRI doser feed into local database"

    def handle(self, *args, **options):
        saved, total = sync_nbri_records()
        self.stdout.write(self.style.SUCCESS(f"Synced {saved} new records out of {total}."))
