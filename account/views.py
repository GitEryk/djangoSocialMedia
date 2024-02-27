from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html",
                  {"section": "dashboard"})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authentication successfully completed ")
                else:
                    return HttpResponse("The account is blocked")
            else:
                return HttpResponse("Incorrect authentication data")
    else:

        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(request, "account/registration_done.html",
                          {"user_form": user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/registration_form.html",
                  {"user_form": user_form})
