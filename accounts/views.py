from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import User

def landing(request):
    return render(request, "landing.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            referral_code = form.cleaned_data.get("referral_code")
            user = form.save(commit=False)
            if referral_code:
                try:
                    inviter = User.objects.get(referral_code=referral_code)
                    user.referred_by = inviter
                except User.DoesNotExist:
                    pass
            user.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
def dashboard(request):
    user = request.user
    template = {
        "student": "dashboard/student_dashboard.html",
        "teacher": "dashboard/teacher_dashboard.html",
        "ceo": "dashboard/ceo_dashboard.html",
    }.get(user.role, "dashboard/student_dashboard.html")
    return render(request, template)
