from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages


def send_login_email(request):
    email = request.POST["email"]
    send_mail(
        "Your login link for Baby's First Words",
        "body text tbc",
        "noreply@babys-first-words",
        [email],
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect("/")


def login(request):
    return redirect("/")
