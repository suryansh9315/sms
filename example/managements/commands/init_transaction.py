from django.core.management.base import BaseCommand
from datetime import datetime
from firebase import db


class Command(BaseCommand):
    help = "Initialise transaction asap fas fas with sample data"

    def handle(self, *args, **kwargs):
        sample_transaction = {
            "transaction_id": "txn123",
            "transaction_amount": 100.00,
            "transaction_date": datetime.now().isoformat(),
            "transaction_given_to": "Tanish",
            "transaction_given_by": "user1",
        }

        transaction_ref = db.collection("transactions").document("txn123")
        transaction_ref.set(sample_transaction)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully initiallised transaction with sample transaction"
            )
        )
