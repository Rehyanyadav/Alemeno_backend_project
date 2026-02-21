from django.core.management.base import BaseCommand
from api.tasks import ingest_customer_data, ingest_loan_data

class Command(BaseCommand):
    help = 'Ingest data from Excel files'

    def handle(self, *args, **options):
        self.stdout.write("Ingesting customer data...")
        ingest_customer_data()
        self.stdout.write("Ingesting loan data...")
        ingest_loan_data()
        self.stdout.write(self.style.SUCCESS("Data ingestion complete!"))
