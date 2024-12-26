from django.core.management.base import BaseCommand
from firebase import db

class Command(BaseCommand):
    help = "Initialise the admin"

    def handle(self, *args, **kwargs):
        admin_data = {
            'image':'',
            'string_value':'',
            'number_value':0
        }
        
        admin_ref =db.collection('admin').document('admin_doc')
        admin_ref.set(admin_data)

        self.stdout.write(self.style.SUCCESS('Successfully initalized admin'))







