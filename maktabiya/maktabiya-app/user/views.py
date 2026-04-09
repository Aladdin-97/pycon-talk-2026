from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.urls import reverse
from user.forms import LoginForm, ProfileForm


import logging

log = logging.getLogger(f"{settings.APP_LOGGER}.{__name__}")
ERR_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"
EMAIL_TEMPLATE_NAME = "Post Booking Mail"


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    context = {"form": form}
    # Check if the 'next' parameter is present in the request's GET parameters
    next_url = request.GET.get("next")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            log.warning(f"Log in Failed: {form.errors}")
            context["msg"] = "Error: Invalid form data!"
            return render(request, "user/login.html", context)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        log.info(f"Log in user: {username}")
        user = authenticate(username=username, password=password)

        if not user:
            log.warning(f"Log in Failed: {username}")
            context["msg"] = "Username or Password is incorrect!"
            return render(request, "user/login.html", context)

        login(request, user)
        log.info(f"Log in successful: {username}")
        if not next_url:
            log.info("Redirecting to homepage index")
            return redirect(reverse("booking:index"))

        log.info(f"Redirecting to the next url: {next_url}")
        return redirect(next_url)

    return render(request, "user/login.html", context)


@require_http_methods(["POST"])
def user_logout(request):
    log.info(f"Log out: {request.user}")
    logout(request)
    return redirect(reverse("user:login"))


@require_http_methods(["GET", "POST"])
@login_required(login_url="/user/login/")
def profile(request):
    user = request.user
    form = ProfileForm(instance=user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user.save()
            msg = "Profile Data Updated Successfully"
            log.info(f"{user} {msg}!")
            messages.success(request, msg, extra_tags="alert alert-info")
        else:
            msg = f"Profile Data Updated Failed: {form.errors}"
            log.error(f"{user} {msg}")
            messages.error(request, msg, extra_tags="alert alert-danger")

        return redirect(reverse("user:profile"))

    return render(request, "user/profile.html", {"form": form, "user": user})
