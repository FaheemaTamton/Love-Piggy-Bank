from fpdf import FPDF
from datetime import date, timedelta
from .models import Savings
from bonding.models import Bonding, Quarrel

def generate_pdf(user):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "💖 Love Piggy Bank Report 💖", ln=True, align="C")
    pdf.ln(10)

    # Fetch stats
    total_savings = sum(s.amount for s in Savings.objects.filter(user=user))
    total_quarrels = Quarrel.objects.filter(user=user).count()
    total_bonding_done = Bonding.objects.filter(user=user, done=True).count()

    # Total weekends missed
    account_creation = user.date_joined.date()
    today = date.today()
    total_weekends = 0
    current = account_creation
    while current <= today:
        if current.weekday() in [5,6]:
            total_weekends += 1
        current += timedelta(days=1)
    total_weekends_missed = total_weekends - total_bonding_done

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Total Savings: ₹{total_savings}", ln=True)
    pdf.cell(0, 10, f"Total Quarrels: {total_quarrels}", ln=True)
    pdf.cell(0, 10, f"Bonding Weekends: Completed {total_bonding_done}, Missed {total_weekends_missed}", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, "“Turning quarrels into love savings! 💕 Keep growing together.”", ln=True)

    return pdf
