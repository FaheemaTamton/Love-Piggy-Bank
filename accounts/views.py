from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, ProfileForm
from bonding.models import Bonding, Quarrel
from savings.models import Savings
from django.contrib.auth.decorators import login_required
from datetime import date

# ----- REGISTER -----
def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Save user
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            # ✅ IMPORTANT: profile already exists (created by signal)
            profile = user.profile

            profile.miss_name = profile_form.cleaned_data['miss_name']
            profile.mister_name = profile_form.cleaned_data['mister_name']
            profile.phone = profile_form.cleaned_data['phone']
            profile.qr_code = profile_form.cleaned_data['qr_code']
            profile.penalty_amount = profile_form.cleaned_data['penalty_amount']
            profile.save()

            return redirect('accounts:login')

    else:
        user_form = RegisterForm()
        profile_form = ProfileForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'accounts/login.html')


# ----- LOGOUT -----
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

# ----- DASHBOARD -----
@login_required
def dashboard(request):
    today = date.today()
    weekend_reminder = False

    # Check weekend bonding reminder
    if today.weekday() in [5, 6]:  # Saturday=5, Sunday=6
        if not Bonding.objects.filter(user=request.user, weekend_date=today).exists():
            weekend_reminder = True

    # Quick stats
    total_bonding_done = Bonding.objects.filter(user=request.user, done=True).count()
    total_quarrels = Quarrel.objects.filter(user=request.user).count()
    total_savings = sum(s.amount for s in Savings.objects.filter(user=request.user))

    context = {
        'weekend_reminder': weekend_reminder,
        'total_bonding_done': total_bonding_done,
        'total_quarrels': total_quarrels,
        'total_savings': total_savings,
    }
    return render(request, 'accounts/dashboard.html', context)

#------PROFILE----------
@login_required
def profile_view(request):
    user_profile = request.user.profile  # assuming your Profile model is linked via OneToOne
    context = {
        'profile': user_profile
    }
    return render(request, 'accounts/profile.html', context)