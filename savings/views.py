from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bonding.models import Bonding, Quarrel
from savings.models import Savings
from datetime import date, timedelta
from django.http import HttpResponse
from .reports import generate_pdf

@login_required
def report(request):
    user = request.user

    # Total savings from Love Piggy Bank
    total_savings = sum(s.amount for s in Savings.objects.filter(user=user))

    # Total quarrels logged
    total_quarrels = Quarrel.objects.filter(user=user).count()

    # Total bonding weekends completed
    total_bonding_done = Bonding.objects.filter(user=user, done=True).count()

    # Total weekends missed
    # Assume we check from account creation date till today
    account_creation = user.date_joined.date()
    today = date.today()
    total_weekends = 0
    current = account_creation
    while current <= today:
        if current.weekday() in [5, 6]:  # Saturday=5, Sunday=6
            total_weekends += 1
        current += timedelta(days=1)

    total_weekends_missed = total_weekends - total_bonding_done

    context = {
        'total_savings': total_savings,
        'total_quarrels': total_quarrels,
        'total_bonding_done': total_bonding_done,
        'total_weekends_missed': total_weekends_missed,
    }

    return render(request, 'savings/report.html', context)

# Optional: Export PDF placeholder
@login_required
def export_pdf(request):
    user = request.user
    pdf = generate_pdf(user)
    response = HttpResponse(pdf.output(dest='S').encode('latin1'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="love_piggy_report_{user.username}.pdf"'
    return response
