from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd
from pdf_maker import generate_bill_pdf
from tkinter import filedialog
import os


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
    return round(energy, 2), round(fixed, 2), round(vat, 2), round(env_fee, 2), round(applied_rates, 2), round(total, 2)


def open_main_app(parent=None, on_logout=None):
    """
    Open the main electric bill calculator application.
    If parent is None, creates a root Tk and runs mainloop (standalone).
    If parent is provided, creates a Frame within parent (for use with account orchestrator).
    on_logout: callback function to call when logout button is clicked (only works in orchestrator mode).
    Returns the Frame containing the app.
    """
    if parent is None:
        # Standalone mode: create root and own the event loop
        win = Tk()
        owns_root = True
        win.title("Electric Bill Calculator")
        win.geometry("400x550")
        frame = Frame(win)
        frame.pack(fill='both', expand=True)
    else:
        # Orchestrator mode: create a frame within parent
        owns_root = False
        frame = Frame(parent)

    # UI Elements (all local to this frame)
    Label(frame, text="Electric Bill Entry", font=("Arial", 16, "bold")).pack(pady=10)

    # NAME
    Label(frame, text="Customer Name:").pack()
    name_entry = Entry(frame, width=30)
    name_entry.pack()

    # ACCOUNT NUMBER
    Label(frame, text="Account Number:").pack()
    acc_entry = Entry(frame, width=30)
    acc_entry.pack()

    # ADDRESS
    Label(frame, text="Address:").pack()
    addr_entry = Entry(frame, width=30)
    addr_entry.pack()

    # CUSTOMER TYPE (Dropdown)
    Label(frame, text="Customer Type:").pack()
    type_box = ttk.Combobox(frame, values=["Residential", "Commercial"], state="readonly")
    type_box.pack()
    type_box.current(0)

    # DATE PICKER
    Label(frame, text="Billing Month:").pack()
    month_entry = DateEntry(frame, width=25, background='darkblue', foreground='white')
    month_entry.pack()

    # UNITS
    Label(frame, text="kWh Used:").pack()
    units_entry = Entry(frame, width=30)
    units_entry.pack()

    # OUTPUT BOX
    output_box = Text(frame, width=50, height=15, state='disabled')
    output_box.pack(pady=10)

    # Local callback functions
    def generate_bill():
        name = name_entry.get()
        account = acc_entry.get()
        address = addr_entry.get()
        customer_type = type_box.get().lower()
        billing_month = month_entry.get()

        try:
            units = float(units_entry.get())
        except Exception:
            output_box.config(state='normal')
            output_box.delete("1.0", END)
            output_box.insert(END, "Invalid kWh input.\n")
            output_box.config(state='disabled')
            return

        energy, fixed, vat, env_fee, applied_rates, total = calculate_bill(units, customer_type)

        # Display Output
        output_box.config(state='normal')
        output_box.delete("1.0", END)
        output_box.insert(END, "=" * 50 + "\n")
        output_box.insert(END, f"Customer Name: {name}\n")
        output_box.insert(END, f"Account Number: {account}\n")
        output_box.insert(END, f"Address: {address}\n")
        output_box.insert(END, f"Consumer Type: {customer_type}\n")
        output_box.insert(END, f"Billing Month: {billing_month}\n")
        output_box.insert(END, "-" * 20 + "\n")
        output_box.insert(END, f"Total kWh Used: {units}\n")
        output_box.insert(END, f"kWh Rate: ₱{applied_rates}/kWh\n")
        output_box.insert(END, f"Fixed Fee: ₱{fixed}\n")
        output_box.insert(END, f"Base Charge: ₱{energy}\n")
        output_box.insert(END, f"Environmental Fee: ₱{env_fee}\n")
        output_box.insert(END, f"VAT (12%): ₱{vat}\n")
        output_box.insert(END, "-" * 20 + "\n")
        output_box.insert(END, f"TOTAL AMOUNT DUE: ₱{total}\n")
        output_box.insert(END, "=" * 50 + "\n")
        output_box.config(state='disabled')

    def download_pdf():
        file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not file:
            return

        try:
            units = float(units_entry.get())
        except Exception:
            output_box.config(state='normal')
            output_box.insert(END, "\nInvalid kWh input for PDF.\n")
            output_box.config(state='disabled')
            return

        customer_type = type_box.get().lower()
        energy, fixed, vat, env_fee, applied_rates, total = calculate_bill(units, customer_type)

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

        generate_bill_pdf(data, file)

    # Buttons
    Button(frame, text="Generate Bill", command=generate_bill, bg="lightgreen").pack(pady=10)
    Button(frame, text="Download PDF", command=download_pdf).pack(pady=5)
    
    # Logout button (only shown in orchestrator mode)
    if not owns_root and callable(on_logout):
        def do_logout():
            on_logout()
        
        Button(frame, text="Logout", command=do_logout, bg="#FF6B6B", fg="white").pack(pady=5)

    if owns_root:
        win = frame.master  # Get the root window
        win.mainloop()
    
    return frame


if __name__ == "__main__":
    open_main_app()
