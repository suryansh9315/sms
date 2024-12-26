from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from firebase import db


class Command(BaseCommand):
    help = "Initialize users in Firestore"

    def handle(self, *args, **kwargs):
        users = [
            {
                "user_id": "1FL",
                "password": make_password("pass1"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "1FR",
                "password": make_password("pass2"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "1BL",
                "password": make_password("pass3"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "1BR",
                "password": make_password("pass4"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "2FL",
                "password": make_password("pass5"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "2FR",
                "password": make_password("pass6"),
                "is_active": True,
                "session_token": "",
                "is_admin": True,
                "pending_amount":0
            },
            {
                "user_id": "2BL",
                "password": make_password("pass7"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "2BR",
                "password": make_password("pass8"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "3FL",
                "password": make_password("pass9"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "3FR",
                "password": make_password("pass10"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "3BL",
                "password": make_password("pass11"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "3BR",
                "password": make_password("pass12"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "4FL",
                "password": make_password("pass13"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "4FR",
                "password": make_password("pass14"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "4BL",
                "password": make_password("pass15"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
            {
                "user_id": "4BR",
                "password": make_password("pass16"),
                "is_active": True,
                "session_token": "",
                "is_admin": False,
                "pending_amount":0
            },
        ]
        for user in users:
            db.collection("users").document(user["user_id"]).set(user)
        self.stdout.write(self.style.SUCCESS("Successfully initialized users"))
