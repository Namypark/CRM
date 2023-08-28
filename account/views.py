import email
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from account.models import Account
from .forms import RegistrationForm


def registerUser(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        print(form.is_valid())

        if form.is_valid():
            print("-----VALID------")
            user = form.save(commit=False)
            user.username = user.email.split("@")[0]
            user.is_active = True
            user.save()

            login(request, user)
            messages.success(request, "user account successfully created")
            return redirect("home")

        else:
            messages.warning(request, "error registering user")
    else:
        messages.info(request, "please register here")
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "register.html", context)
    #         first_name = form.cleaned_data["first_name"]
    #         print(first_name)
    #         email = form.cleaned_data["email"]
    #         last_name = form.cleaned_data["last_name"]
    #         phone_number = form.cleaned_data["phone_number"]
    #         password = form.cleaned_data["password1"]
    #         print(password)
    #         password2 = form.cleaned_data["password2"]
    #         print(password2)
    #         username = email.split("@")[0]
    #         if password and password2 and password != password2:
    #             form.add_error("password2", "passwords do not match")
    #             messages.error(request, "Passwords do not match")
    #         user = Account.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             email=email,
    #             phone_number=phone_number,
    #             password=password,
    #             username=username,
    #         )
    #         return redirect("login")
    #     else:
    #         messages.error(request, "error creating account")
    #         print("Invalid")
    # else:
    #     messages.info(request, "Please Register here")
    #     form = RegistrationForm()


@csrf_protect
# Create your views here.
def loginUser(request):
    if request.method == "POST":
        # do something
        email = request.POST.get("email")
        print(email)
        password = request.POST.get("password")
        print(password)
        try:
            user = Account.objects.get(email=email)
            print("--try block--")
            print(user.email)
            print(user.password)
        except Account.DoesNotExist:
            messages.error(request, "Check your email address or password")
            return redirect("login")

        auth = authenticate(request, email=email, password=password)
        print(auth)
        if auth is not None:
            login(request, auth)
            messages.success(request, f"welcome back {user.first_name}")
            return redirect("home")
        else:
            messages.warning(request, "Please check your email address or password")
            return redirect("login")

    return render(request, "login.html")


def logoutUser(request):
    logout(request)
    messages.success(request, "logged out successful")
    print("logged out successfully")
    return redirect("login")
