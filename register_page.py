"""register_page.py

Provides a function to build the registration frame so this UI can be
embedded inside a larger application instead of running at import time.
"""
from tkinter import Frame, Label, Button, Entry, PhotoImage, StringVar, messagebox
import sqlite3
from Database import db_utils


def build_register_frame(parent, db_path, on_show_login=None, on_register_success=None):
    """Create and return a Frame containing the registration UI.

    parent: parent widget (usually a Frame or Tk)
    db_path: path to sqlite database file
    on_show_login: callback to switch to login screen
    on_register_success: callback when registration is successful
    """
    frame = Frame(parent, bg="#525561")

    # Keep references to images on the frame to avoid garbage collection
    frame._backgroundImage = PhotoImage(file="assets/image_1.png")
    bg_image = Label(frame, image=frame._backgroundImage, bg="#525561")
    bg_image.place(x=120, y=28)

    frame._headerText_image_left = PhotoImage(file="assets/headerText_image.png")
    headerText_image_label1 = Label(bg_image, image=frame._headerText_image_left, bg="#272A37")
    headerText_image_label1.place(x=60, y=45)

    headerText1 = Label(bg_image, text="Electric Bill Calculator", fg="#FFFFFF",
                        font=("yu gothic ui bold", 20 * -1), bg="#272A37")
    headerText1.place(x=110, y=45)

    # small link to show login (hook provided by orchestrator)
    if callable(on_show_login):
        switchLogin = Button(bg_image, text="Login", fg="#206DB4",
                             font=("yu gothic ui Bold", 15 * -1), bg="#272A37",
                             bd=0, cursor="hand2", activebackground="#272A37",
                             activeforeground="#ffffff", command=on_show_login)
        switchLogin.place(x=230, y=185, width=50, height=35)

    createAccount_header = Label(bg_image, text="Create new account", fg="#FFFFFF",
                                 font=("yu gothic ui Bold", 28 * -1), bg="#272A37")
    createAccount_header.place(x=75, y=121)

    # Input variables
    first_var = StringVar()
    last_var = StringVar()
    email_var = StringVar()
    pwd_var = StringVar()
    confirm_var = StringVar()

    # First / Last name inputs (compact version of original layout)
    frame._first_img = PhotoImage(file="assets/input_img.png")
    first_container = Label(bg_image, image=frame._first_img, bg="#272A37")
    first_container.place(x=80, y=242)
    Label(first_container, text="First name", fg="#FFFFFF", font=("yu gothic ui SemiBold", 13 * -1),
          bg="#3D404B").place(x=25, y=0)
    Entry(first_container, bd=0, bg="#3D404B", highlightthickness=0, font=("yu gothic ui SemiBold", 16 * -1),
          textvariable=first_var).place(x=8, y=17, width=140, height=27)

    last_container = Label(bg_image, image=frame._first_img, bg="#272A37")
    last_container.place(x=293, y=242)
    Label(last_container, text="Last name", fg="#FFFFFF", font=("yu gothic ui SemiBold", 13 * -1),
          bg="#3D404B").place(x=25, y=0)
    Entry(last_container, bd=0, bg="#3D404B", highlightthickness=0, font=("yu gothic ui SemiBold", 16 * -1),
          textvariable=last_var).place(x=8, y=17, width=140, height=27)

    # Email
    frame._email_img = PhotoImage(file="assets/email.png")
    email_container = Label(bg_image, image=frame._email_img, bg="#272A37")
    email_container.place(x=80, y=311)
    Label(email_container, text="Email account", fg="#FFFFFF", font=("yu gothic ui SemiBold", 13 * -1),
          bg="#3D404B").place(x=25, y=0)
    Entry(email_container, bd=0, bg="#3D404B", highlightthickness=0, font=("yu gothic ui SemiBold", 16 * -1),
          textvariable=email_var).place(x=8, y=17, width=354, height=27)

    # Password
    frame._pwd_img = PhotoImage(file="assets/input_img.png")
    pwd_container = Label(bg_image, image=frame._pwd_img, bg="#272A37")
    pwd_container.place(x=80, y=380)
    Label(pwd_container, text="Password", fg="#FFFFFF", font=("yu gothic ui SemiBold", 13 * -1),
          bg="#3D404B").place(x=25, y=0)
    Entry(pwd_container, bd=0, bg="#3D404B", highlightthickness=0, font=("yu gothic ui SemiBold", 16 * -1),
          textvariable=pwd_var, show='•').place(x=8, y=17, width=140, height=27)

    confirm_container = Label(bg_image, image=frame._pwd_img, bg="#272A37")
    confirm_container.place(x=293, y=380)
    Label(confirm_container, text="Confirm Password", fg="#FFFFFF",
          font=("yu gothic ui SemiBold", 13 * -1), bg="#3D404B").place(x=25, y=0)
    Entry(confirm_container, bd=0, bg="#3D404B", highlightthickness=0, font=("yu gothic ui SemiBold", 16 * -1),
          textvariable=confirm_var, show='•').place(x=8, y=17, width=140, height=27)

    # Submit
    frame._submit_img = PhotoImage(file="assets/button_1.png")

    def signup():
        # basic validation
        if not (first_var.get().strip() and last_var.get().strip() and email_var.get().strip() and confirm_var.get().strip()):
            messagebox.showerror("Error", "All Fields are Required")
            return
        if pwd_var.get() != confirm_var.get():
            messagebox.showerror("Error", "Password and Confirm Password didn't match")
            return

        try:
            conn = sqlite3.connect(db_path)
            db_utils.create_account(conn, first_var.get().strip(), last_var.get().strip(), email_var.get().strip(), pwd_var.get())
            conn.close()
            # clear
            first_var.set("")
            last_var.set("")
            email_var.set("")
            pwd_var.set("")
            confirm_var.set("")
            messagebox.showinfo('Success', "New Account Created Successfully :)")
            # Call success callback if provided
            if callable(on_register_success):
                on_register_success()
        except Exception:
            messagebox.showerror("Error", "Something went wrong, please try again :(")

    submit_button = Button(bg_image, image=frame._submit_img, borderwidth=0, highlightthickness=0,
                           relief="flat", activebackground="#272A37", cursor="hand2", command=signup)
    submit_button.place(x=130, y=460, width=333, height=65)

    # small footer
    frame._footer_img = PhotoImage(file="assets/headerText_image.png")
    Label(bg_image, image=frame._footer_img, bg="#272A37").place(x=650, y=530)
    Label(bg_image, text="Luke Ezekiel B. Abad", fg="#FFFFFF", font=("yu gothic ui bold", 20 * -1),
          bg="#272A37").place(x=700, y=530)

    return frame


if __name__ == "__main__":
    # Quick manual run for development
    from tkinter import Tk

    root = Tk()
    root.geometry('1240x650+100+100')
    frm = build_register_frame(root, "Database/AccountSystem.db")
    frm.pack(fill='both', expand=True)
    root.mainloop()
