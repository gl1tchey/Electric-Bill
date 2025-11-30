from tkinter import *
from tkinter import ttk
try:
    from tkcalendar import DateEntry
except:
    from tkinter import Entry as DateEntry
from pdf_maker import generate_bill_pdf
from tkinter import filedialog


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
        tiers = [(50, 5.0), (50, 6.5), (100, 8.0), (float("inf"), 10.0)]
        fixed = 40
    else:
        tiers = [(100, 3.5), (200, 5.0), (500, 6.5), (float("inf"), 7.5)]
        fixed = 100

    energy, applied_rates = tiered(units, tiers)
    vat = energy * 0.12
    env_fee = energy * 0.0025
    total = energy + fixed + vat + env_fee
    return (
        round(energy, 2),
        round(fixed, 2),
        round(vat, 2),
        round(env_fee, 2),
        round(applied_rates, 2),
        round(total, 2),
    )


def open_main_app(parent=None, on_logout=None):

    owns_root = False
    if parent is None:
        root = Tk()
        owns_root = True
        root.title("Electric Bill Calculator")
        root.geometry("1150x720")
        root.minsize(950, 620)
        root.configure(bg="#1F2125")
        container = Frame(root, bg="#1F2125")
        container.pack(fill="both", expand=True)
        build_parent = container
    else:
        build_parent = parent

    main_frame = Frame(build_parent, bg="#1F2125")
    main_frame.pack(fill="both", expand=True)

    card = Frame(main_frame, bg="#26282F", bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.9)

    header = Frame(card, bg="#26282F")
    header.pack(fill="x", padx=26, pady=(20, 10))

    Label(
        header,
        text="Electric Bill Entry",
        fg="#FFFFFF",
        bg="#26282F",
        font=("Yu Gothic UI Bold", 20),
    ).pack(anchor="w")

    Label(
        header,
        text="Bill Calculator",
        fg="#BFC2C7",
        bg="#26282F",
        font=("Yu Gothic UI", 14),
    ).pack(anchor="w", pady=(4, 0))

    scroll_container = Frame(card, bg="#26282F")
    scroll_container.pack(fill="both", expand=True, padx=26)

    canvas = Canvas(
        scroll_container,
        bg="#26282F",
        highlightthickness=0,
        bd=0
    )
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(
        scroll_container, orient="vertical", command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    form_frame = Frame(canvas, bg="#26282F")
    canvas.create_window((0, 0), window=form_frame, anchor="nw")

    def update_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    form_frame.bind("<Configure>", update_scroll)

    left = Frame(form_frame, bg="#26282F")
    right = Frame(form_frame, bg="#26282F")

    left.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
    right.grid(row=0, column=1, sticky="nsew")

    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)

    def make_label(parent, text):
        return Label(
            parent,
            text=text,
            fg="#FFFFFF",
            bg="#26282F",
            font=("Yu Gothic UI Semibold", 12),
        )

    def make_entry(parent):
        e = Entry(
            parent,
            bd=0,
            bg="#32343C",
            fg="#FFFFFF",
            font=("Yu Gothic UI Semibold", 12),
            insertbackground="#FFFFFF",
        )
        e.pack(fill="x", pady=(6, 14), ipady=8)
        return e

    make_label(left, "Customer Name").pack(anchor="w")
    name_entry = make_entry(left)

    make_label(left, "Account Number").pack(anchor="w")
    acc_entry = make_entry(left)

    make_label(left, "Address").pack(anchor="w")
    addr_entry = make_entry(left)

    make_label(left, "Customer Type").pack(anchor="w")
    type_box = ttk.Combobox(
        left,
        values=["Residential", "Commercial"],
        state="readonly",
        font=("Yu Gothic UI", 11),
    )
    type_box.current(0)
    type_box.pack(fill="x", pady=(6, 14), ipady=5)

    make_label(left, "Billing Month").pack(anchor="w")
    month_entry = DateEntry(
        left,
        background="#206DB4",
        foreground="white",
        font=("Yu Gothic UI", 11),
    )
    month_entry.pack(fill="x", pady=(6, 14), ipady=5)

    make_label(right, "kWh Used").pack(anchor="w")
    units_entry = make_entry(right)

    make_label(right, "Bill Summary").pack(anchor="w")
    output_frame = Frame(right, bg="#34363D")
    output_frame.pack(fill="both", expand=True, pady=(6, 14))
    output_box = Text(
        output_frame,
        bg="#2D2F35",
        fg="#F1F1F1",
        font=("Yu Gothic UI", 11),
        state="disabled",
        relief="flat",
        bd=0,
        wrap="word",
    )
    output_box.pack(fill="both", expand=True, padx=10, pady=10)

    bottom_buttons = Frame(card, bg="#26282F")
    bottom_buttons.pack(side="bottom", pady=18)

    def set_placeholder(entry, text):
        placeholder_color = "#888888"
        normal_color = entry.cget("fg")

        def on_focus_in(e):
            if entry.get() == text:
                entry.delete(0, END)
                entry.config(fg=normal_color)

        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg=placeholder_color)

        entry.insert(0, text)
        entry.config(fg=placeholder_color)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    set_placeholder(name_entry, "Customer Name")
    set_placeholder(acc_entry, "Account Number")
    set_placeholder(addr_entry, "Address")
    set_placeholder(units_entry, "kWh Used")

    def generate_bill():
        try:
            units = float(units_entry.get())
        except:
            output_box.config(state="normal")
            output_box.delete("1.0", END)
            output_box.insert(END, "Invalid kWh input.\n")
            output_box.config(state="disabled")
            return

        ctype = type_box.get().lower()
        energy, fixed, vat, env_fee, applied_rates, total = calculate_bill(
            units, ctype
        )

        output_box.config(state="normal")
        output_box.delete("1.0", END)
        output_box.insert(END, f"Customer: {name_entry.get()}\n")
        output_box.insert(END, f"Account: {acc_entry.get()}\n")
        output_box.insert(END, f"Type: {ctype}\n")
        output_box.insert(END, f"Month: {month_entry.get()}\n")
        output_box.insert(END, "-" * 35 + "\n")
        output_box.insert(END, f"kWh: {units}\n")
        output_box.insert(END, f"Rate: P{applied_rates}\n")
        output_box.insert(END, f"Fixed Charge: P{fixed}\n")
        output_box.insert(END, f"Base: P{energy}\n")
        output_box.insert(END, f"Env. Fee: P{env_fee}\n")
        output_box.insert(END, f"VAT: P{vat}\n")
        output_box.insert(END, "-" * 35 + "\n")
        output_box.insert(END, f"TOTAL: P{total}\n", "total")
        output_box.tag_config(
            "total",
            foreground="#58C27A",
            font=("Yu Gothic UI Bold", 12)
        )
        output_box.config(state="disabled")

    def download_pdf():
        try:
            units = float(units_entry.get())
        except:
            return

        ctype = type_box.get().lower()
        energy, fixed, vat, env_fee, applied_rates, total = calculate_bill(
            units, ctype
        )

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
            "total": total,
        }

        file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not file:
            return
        generate_bill_pdf(data, file)

    def logout_action():
        if on_logout:
            on_logout()
        else:
            try:
                build_parent.winfo_toplevel().destroy()
            except:
                pass

    btn_style = {"font": ("Yu Gothic UI", 11, "bold"), "bd": 0, "relief": "flat", "cursor": "hand2", "width": 14, "height": 1}

    Button(
        bottom_buttons,
        text="Generate Bill",
        command=generate_bill,
        bg="#58C27A",
        fg="#FFFFFF",
        **btn_style
    ).pack(side="left", padx=10)

    Button(
        bottom_buttons,
        text="Download PDF",
        command=download_pdf,
        bg="#206DB4",
        fg="#FFFFFF",
        **btn_style
    ).pack(side="left", padx=10)

    Button(
        bottom_buttons,
        text="Logout",
        command=logout_action,
        bg="#FF6B6B",
        fg="#FFFFFF",
        **btn_style
    ).pack(side="left", padx=10)

    if owns_root:
        root.mainloop()


if __name__ == "__main__":
    open_main_app()
