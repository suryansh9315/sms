from django.shortcuts import render, redirect
from firebase import db, bucket
from django.contrib.auth.hashers import check_password
import secrets
# from example.data import users_data
from django.contrib import messages
from django.core.paginator import Paginator
from firebase_admin import firestore
import datetime

from django.utils.dateparse import parse_datetime
# import io
import os
import tempfile


def login_view(request):
    error_message = None
    user_authenticated = False
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        user = db.collection("users").document(user_id).get().to_dict()
        # print(password,user['password'])
        if user and check_password(password, user["password"]):
            session_token = secrets.token_hex(16)
            db.collection("users").document(user_id).update(
                {"session_token": session_token}
            )
            response = redirect("logbook")
            print("user logged in", user_authenticated)
            response.set_cookie("session_token", session_token)
            print("with session : ", session_token)
            return response
        else:
            error_message = "invalid credentials. please try again!"

    return render(
        request,
        "login.html",
        {"error_message": error_message, "user_authenticated": user_authenticated},
    )


def admin_view(request):
    session_token = request.COOKIES.get("session_token")
    user = db.collection("users").where("session_token", "==", session_token).get()
    user_data = user[0].to_dict()
    if user_data["is_admin"]:
        print("admin hu mai")
        user_authenticated = True
        if request.method == "POST":
            counter_doc_ref = db.collection("counters").document("transaction_counter")
            counter_doc = counter_doc_ref.get()
            last_number = counter_doc.to_dict().get("last_number", 0)
            next_number = last_number + 1
            transaction_id = f"txn{next_number}"

            counter_doc_ref.update({"last_number": next_number})

            transaction_amount = float(request.POST.get("transaction_amount"))
            transaction_date = request.POST.get("transaction_date")
            transaction_given_to = request.POST.get("transaction_given_to")
            transaction_given_by = request.POST.get("transaction_given_by")
            settle_checkbox = request.POST.get("settle_checkbox") == "on"

            transaction_settle = False

            if settle_checkbox:
                transaction_settle = True
                divided_amount = transaction_amount / 16
                users = db.collection("users").stream()
                for user in users:
                    user_ref = user.reference
                    user_data = user.to_dict()
                    new_balance = user_data.get("pending_amount", 0) + divided_amount
                    user_ref.update({"pending_amount": new_balance})
                    message = "transaction done!"

            # Save transaction to Firestore
            db.collection("transactions").document(transaction_id).set(
                {
                    "transaction_id": transaction_id,
                    "transaction_amount": transaction_amount,
                    "transaction_date": transaction_date,
                    "transaction_given_to": transaction_given_to,
                    "transaction_given_by": transaction_given_by,
                    "transaction_settle": transaction_settle,
                }
            )
            messages.success(request, "Transaction added successfully!")
        return render(request, "admin.html", {"user_authenticated": user_authenticated})
    else:
        return redirect(request, "logbook")


def user_data(request):
    session_token = request.COOKIES.get("session_token")
    user = db.collection("users").where("session_token", "==", session_token).get()
    user_data = user[0].to_dict()
    if user_data["is_admin"]:
        print("admin hu mai")
        user_authenticated = True
        user_is_admin = True
        if request.method == "POST":
            user_id = request.POST.get("user_id")
            pending_amount = float(request.POST.get("pending_amount"))
            is_active = request.POST.get("is_active") == "on"

            user_ref = db.collection("users").document(user_id)
            user_ref.update({"pending_amount": pending_amount, "is_active": is_active})
            messages.success(request, "user data updated successfully")
            return redirect("user_data")

        users = db.collection("users").stream()
        user_list = []
        for user in users:
            user_data = user.to_dict()
            user_data["user_id"] = user.id
            user_list.append(user_data)

        return render(
            request,
            "userData.html",
            {
                "users": user_list,
                "user_authenticated": user_authenticated,
                "user_is_admin": user_is_admin,
            },
        )


def admin_info(request):
    session_token = request.COOKIES.get("session_token")
    user = db.collection("users").where("session_token", "==", session_token).get()
    user_data = user[0].to_dict()
    if user_data["is_admin"]:
        print("admin hu mai")
        user_authenticated = True
        user_is_admin = True
        if request.method == "POST":
            image = request.FILES["image"]
            phone = request.POST.get("number_value")
            upi_id = request.POST.get("string_value")

            temp_file = tempfile.NamedTemporaryFile(delete=False)
            for chunk in image.chunks():
                temp_file.write(chunk)
            temp_file.close()

            blob = bucket.blob(f"admin/{image.name}")
            blob.upload_from_filename(temp_file.name)
            os.remove(temp_file.name)

            image_url = blob.public_url
            admin_doc = db.collection("admin").document("admin_doc")
            admin_doc.set(
                {
                    "image": image_url,
                    "phone": phone,
                    "upiId": upi_id,
                }
            )

    return render(
        request,
        "adminInfo.html",
        {"user_authenticated": user_authenticated, "user_is_admin": user_is_admin},
    )


def logbook_view(request):
    session_token = request.COOKIES.get("session_token")
    user = db.collection("users").where("session_token", "==", session_token).get()
    user_data = user[0].to_dict()
    if not user:
        return redirect("login")
    else:
        user_authenticated = True

    if user_data["is_admin"]:
        user_is_admin = True
    else:
        user_is_admin = False

    transactions_ref = db.collection("transactions").order_by(
        "transaction_date", direction=firestore.Query.DESCENDING
    )
    transactions = [doc.to_dict() for doc in transactions_ref.stream()]

    admin_doc = db.collection("admin").document("admin_doc").get().to_dict()
    admin_payment_info = {
        "image": admin_doc.get("image") if admin_doc else "",
        "phone": admin_doc.get("phone") if admin_doc else "",
        "upiid": admin_doc.get("upiId") if admin_doc else "",
    }

    image_path = admin_payment_info["image"].split("admin/")[-1]
    print(image_path)

    if image_path:
        blob = bucket.blob("admin/" + image_path)
        url = blob.generate_signed_url(expiration=datetime.timedelta(hours=1))
    else:
        url = ""

    paginator = Paginator(transactions, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "user": user,
        "pending_amount": user_data.get("pending_amount", 0),
        "user_authenticated": user_authenticated,
        "user_is_admin": user_is_admin,
        "admin_payment_info": admin_payment_info,
        "url": url,
    }

    return render(request, "logbook.html", context)


def logout_view(request):
    session_token = request.COOKIES.get("session_token")
    if session_token:
        user = db.collection("users").where("session_token", "==", session_token).get()
        if user:
            user_id = user[0].id
            db.collection("users").document(user_id).update({"session_token": ""})

    user_authenticated = False
    response = redirect("login")
    response.delete_cookie("session_token")
    print("userlogged out ", user_authenticated)
    return response
