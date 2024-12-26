from django.core.management.base import BaseCommand
from firebase import db
class Command(BaseCommand):
    help = 'Initialize the transaction counter in Firebase'

    def handle(self, *args, **kwargs):        
        doc_ref = db.collection('counters').document('transaction_counter')
        if not doc_ref.get().exists:
            doc_ref.set({'last_number': 0})
            self.stdout.write(self.style.SUCCESS('Initialized transaction counter.'))
        else:
            self.stdout.write(self.style.SUCCESS('Transaction counter already initialized.'))
