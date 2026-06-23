from fpdf import FPDF
from .models import Savings

def generate_report(user, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200,10,txt="Love Piggy Bank Report",ln=True,align="C")

