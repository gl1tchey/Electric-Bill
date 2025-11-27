# pdf_generator.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

def generate_bill_pdf(data, file_name="ElectricBill.pdf"):
    pdf = SimpleDocTemplate(file_name, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title = Paragraph("<b><font size=16>Electricity Billing Reciept</font></b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Customer Info Table
    customer_table = [
        ["Customer Name:", data["name"]],
        ["Account Number:", data["account"]],
        ["Address:", data["address"]],
        ["Consumer Type:", data["type"]],
        ["Billing Month:", data["month"]],
    ]

    table = Table(customer_table, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Billing info table
    bill_table = [
        ["Total kWh Used", data["kwh"]],
        ["Applied Rate", f"₱{data['rate']}/kWh"],
        ["Fixed Charge", f"₱{data['fixed']}"],
        ["Base Charge", f"₱{data['base']}"],
        ["Environmental Fee", f"₱{data['env']}"],
        ["VAT (12%)", f"₱{data['vat']}"],
        ["TOTAL AMOUNT DUE", f"₱{data['total']}"],
    ]

    billbox = Table(bill_table, colWidths=[200, 250])
    billbox.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,6), (-1,6), colors.lightgrey),
        ('FONT', (0,6), (-1,6), 'Helvetica-Bold', 12),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
    ]))

    elements.append(billbox)

    pdf.build(elements)
