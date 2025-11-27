from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd
from pdf_maker import generate_bill_pdf
from tkinter import filedialog
import os
import urllib.request
from tkinter.scrolledtext import ScrolledText

root = Tk()
root.title("Electric Bill Calculator")
root.geometry("400x550")



def open_main_app():
    main_win = tk.Toplevel()
    main_win.title("Main Application")
    main_win.geometry("600x400")
    tk.Label(main_win, text="Welcome!", font=("Arial", 16)).pack(pady=50)



# -------------------- FUNCTIONS --------------------
def tiered(u, tiers):
    cost = 0
    applied_rates = 0
    for limits, rate in tiers:
        if u <= 0:
            break
        use = min(u, limits)
        cost += use * rate
        applied_rates = rate
        u -= use
    return cost, applied_rates

def calculate_bill(units, customer_type):
    if customer_type == "residential":
        tiers = [
            (50, 5.0),
            (50, 6.5),
            (100, 8.0),
            (float("inf"), 10.0),
        ]
        fixed = 40
    else:
        tiers = [
            (100, 3.5),
            (200, 5.0),
            (500, 6.5),
            (float("inf"), 7.5),
        ]
        fixed = 100

    energy, applied_rates = tiered(units, tiers)
    vat = energy * 0.12
    env_fee = energy * 0.0025
    total = energy + fixed + vat + env_fee
    return round(energy,2), round(fixed,2), round(vat,2), round(env_fee,2), round(applied_rates,2), round(total,2)

def generate_bill():
    name = name_entry.get()
    account = acc_entry.get()
    address = addr_entry.get()
    customer_type = type_box.get().lower()
    billing_month = month_entry.get()

    try:
        units = float(units_entry.get())
    except:
        output_box.config(state='normal')
        output_box.delete("1.0", END)
        output_box.insert(END, "Invalid kWh input.\n")
        output_box.config(state='disabled')
        return

    energy, fixed, vat, env_fee, applied_rates, total = calculate_bill(units, customer_type)

    # Display Output
    output_box.config(state='normal')
    output_box.delete("1.0", END)
    output_box.insert(END, "="*50 + "\n")
    output_box.insert(END, f"Customer Name: {name}\n")
    output_box.insert(END, f"Account Number: {account}\n")
    output_box.insert(END, f"Address: {address}\n")
    output_box.insert(END, f"Consumer Type: {customer_type}\n")
    output_box.insert(END, f"Billing Month: {billing_month}\n")
    output_box.insert(END, "-"*20 + "\n")
    output_box.insert(END, f"Total kWh Used: {units}\n")
    output_box.insert(END, f"kWh Rate: ₱{applied_rates}/kWh\n")
    output_box.insert(END, f"Fixed Fee: ₱{fixed}\n")
    output_box.insert(END, f"Base Charge: ₱{energy}\n")
    output_box.insert(END, f"Environmental Fee: ₱{env_fee}\n")
    output_box.insert(END, f"VAT (12%): ₱{vat}\n")
    output_box.insert(END, "-"*20 + "\n")
    output_box.insert(END, f"TOTAL AMOUNT DUE: ₱{total}\n")
    output_box.insert(END, "="*50 + "\n")
    output_box.config(state='disabled')









#----------Saving to pdf----------------------
def download_pdf():
    file = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not file:
        return  # user input cancelled
    base_name = "Electric Bill Reciept"
    # Handle duplicate filenames
    base_name, ext = os.path.splitext(file)
    counter = 0
    temp_file = file
    while os.path.exists(temp_file):
        counter += 1
        temp_file = f"{base_name}({counter}){ext}"
    file = temp_file

    # Get billing data
    try:
        units = float(units_entry.get())
    except:
        output_box.config(state='normal')
        output_box.insert(END, "\nInvalid kWh input for PDF.\n")
        output_box.config(state='disabled')
        return

    customer_type = type_box.get().lower()
    energy, fixed, vat, env_fee, applied_rates, total = calculate_bill(units, customer_type)

    # Prepare data dictionary
    data = {
        "name": name_entry.get(),
        "account": acc_entry.get(),
        "address": addr_entry.get(),
        "type": type_box.get(),
        "month": month_entry.get(),
        "kwh": units,
        "rate": applied_rates,
        "fixed": fixed,
        "base": energy,
        "env": env_fee,
        "vat": vat,
        "total": total
    }

    # Generate PDF
    generate_bill_pdf(data, file)












# -------------------- UI ELEMENTS --------------------
Label(root, text="Electric Bill Entry", font=("Arial", 16, "bold")).pack(pady=10)

# NAME
Label(root, text="Customer Name:").pack()
name_entry = Entry(root, width=30)
name_entry.pack()

# ACCOUNT NUMBER
Label(root, text="Account Number:").pack()
acc_entry = Entry(root, width=30)
acc_entry.pack()

# ADDRESS
Label(root, text="Address:").pack()
addr_entry = Entry(root, width=30)
addr_entry.pack()

# CUSTOMER TYPE (Dropdown)
Label(root, text="Customer Type:").pack()
type_box = ttk.Combobox(root, values=["Residential", "Commercial"], state="readonly")
type_box.pack()
type_box.current(0)

# DATE PICKER
Label(root, text="Billing Month:").pack()
month_entry = DateEntry(root, width=25, background='darkblue', foreground='white')
month_entry.pack()

# UNITS
Label(root, text="kWh Used:").pack()
units_entry = Entry(root, width=30)
units_entry.pack()

# BUTTON
Button(root, text="Generate Bill", command=generate_bill, bg="lightgreen").pack(pady=10)

# OUTPUT BOX
output_box = Text(root, width=50, height=15, state='disabled')
output_box.pack(pady=10)
#For PDF download
Button(root, text="Download PDF", command=download_pdf).pack()



root.mainloop()
