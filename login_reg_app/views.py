from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt


def index(request):
    context = {"users": User.objects.all()}
    return render(request, "index.html", context)


def register_user(request):

    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")

    password = request.POST["password"]
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        password=pw_hash,
    )
    return redirect("/")


def check_login(request):
    user = User.objects.filter(email=request.POST["email"])
    if user:  # if True (email is found with registration database)
        logged_user = user[0]
        if bcrypt.checkpw(
            request.POST["password"].encode(), logged_user.password.encode()
        ):
            request.session["userid"] = logged_user.id
            print(logged_user.id)
            return redirect(f"/success/{logged_user.id}")
        return redirect("/")


def success_page(request, user_id):
    context = {
        "user": User.objects.get(id=user_id),
    }
    return render(request, "success.html", context)


def logout_user(request):
    del request.session["userid"]
    return redirect("/")
