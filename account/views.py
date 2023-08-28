from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from account.models import Account
from .forms import RegistrationForm


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
        except:
            messages.error(request, "Check your email address or password")
            return redirect("login")

        auth = authenticate(request, email=user.email, password=password)
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


def registerUser(request):
    if request.method == "POST":
        forms = RegistrationForm(request.POST)

        print(forms)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.username = user.email.split("@")[0]
            print(user.username)
            email = user.email
            user.save()
            return redirect("login")

        else:
            messages.error(request, "error creating account")
    else:
        messages.info(request, "Please Register here")
        forms = RegistrationForm()

    context = {"forms": forms}
    return render(request, "register.html", context)
