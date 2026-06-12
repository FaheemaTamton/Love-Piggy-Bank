from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Bonding
from savings.models import Savings
from .models import Quarrel

@login_required
def bonding_view(request):
    user = request.user
    today = date.today()

    # Allow only Saturday & Sunday
    if today.weekday() not in [5, 6]:
        return render(request, 'bonding/bonding.html', {
            'not_weekend': True
        })

    # Check if already logged for this weekend
    already_logged = Bonding.objects.filter(
        user=user,
        weekend_date=today
    ).exists()

    if already_logged:
        return render(request, 'bonding/bonding.html', {
            'already_logged': True
        })

    error_message = None

    if request.method == "POST":
        choice = request.POST.get('bonding_option')

        if not choice:
            error_message = "Please select an option before submitting."
        else:
            if choice == "yes":
                Bonding.objects.create(
                    user=user,
                    weekend_date=today,
                    done=True
                )
                return redirect('accounts:dashboard')

            elif choice == "no":
                Bonding.objects.create(
                    user=user,
                    weekend_date=today,
                    done=False
                )
                Savings.objects.create(
                    user=user,
                    amount=user.profile.penalty_amount,
                    reason='bonding'
                )
                return redirect('accounts:dashboard')

    return render(request, 'bonding/bonding.html', {
        'error_message': error_message
    })

@login_required
def quarrel_view(request):
    user = request.user

    # FINAL CONFIRMATION
    if request.method == "POST" and request.POST.get("confirm_payment"):
        reason = request.session.get("quarrel_reason")

        Quarrel.objects.create(user=user, reason=reason)
        Savings.objects.create(
            user=user,
            amount=user.profile.penalty_amount,
            reason="quarrel"
        )

        request.session.pop("quarrel_reason", None)
        return redirect("accounts:dashboard")
    

    if request.method == "POST":
        confirm = request.POST.get("confirm")
        reason = request.POST.get("reason")

        if not confirm:
            return render(request, "bonding/quarrel.html", {
                "error": "Please select Yes or No."
            })

        if confirm == "no":
            return redirect("accounts:dashboard")

        if not reason:
            return render(request, "bonding/quarrel.html", {
                "error": "Please enter a reason."
            })

        request.session["quarrel_reason"] = reason
        return render(request, "bonding/quarrel.html", {
            "show_qr": True
        })

    return render(request, "bonding/quarrel.html")
