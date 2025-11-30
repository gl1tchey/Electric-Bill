try:
    # Try to import reportlab; if it's available, keep the full PDF generator
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter


    def generate_bill_pdf(data, file_name="ElectricBill.pdf"):
        pdf = SimpleDocTemplate(file_name, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        title = Paragraph("<b><font size=16>Electricity Billing Receipt</font></b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Customer Info Table
        customer_table = [
            ["Customer Name:", data.get("name", "")],
            ["Account Number:", data.get("account", "")],
            ["Address:", data.get("address", "")],
            ["Consumer Type:", data.get("type", "")],
            ["Billing Month:", data.get("month", "")],
        ]

        table = Table(customer_table, colWidths=[150, 300])
        table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        # Billing info table
        bill_table = [
            ["Total kWh Used", data.get("kwh", "")],
            ["Applied Rate", f"₱{data.get('rate', '')}/kWh"],
            ["Fixed Charge", f"₱{data.get('fixed', '')}"],
            ["Base Charge", f"₱{data.get('base', '')}"],
            ["Environmental Fee", f"₱{data.get('env', '')}"],
            ["VAT (12%)", f"₱{data.get('vat', '')}"],
            ["TOTAL AMOUNT DUE", f"₱{data.get('total', '')}"],
        ]

        billbox = Table(bill_table, colWidths=[200, 250])
        billbox.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 6), (-1, 6), colors.lightgrey),
            ('FONT', (0, 6), (-1, 6), 'Helvetica-Bold', 12),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elements.append(billbox)

        pdf.build(elements)
except Exception:
    # reportlab not available — provide a fallback that writes a plain text file
    def generate_bill_pdf(data, file_name="ElectricBill.txt"):
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write('Electricity Billing Receipt\n')
                f.write('=' * 40 + '\n')
                for k in ("name", "account", "address", "type", "month"):
                    f.write(f"{k.capitalize()}: {data.get(k, '')}\n")
                f.write('\n')
                f.write('Charges:\n')
                for k in ("kwh", "rate", "fixed", "base", "env", "vat", "total"):
                    f.write(f"{k}: {data.get(k, '')}\n")
                f.write('=' * 40 + '\n')
        except Exception:
            # If even the fallback fails, silently ignore — don't crash the UI
            pass
