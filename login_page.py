from tkinter import *
import sqlite3
from Database import db_utils


def build_login_frame(parent, db_path, on_login_success=None, on_show_register=None):
    """Build the original login UI inside the provided `parent` Frame.

    This reproduces the original look that used `assets/image_1.png` and
    absolute placements. The function returns a Frame that can be packed or
    placed by the caller. If `parent` is a Tk root the frame will behave as
    a standalone window region; otherwise it will fill the provided container.
    """
    frame = Frame(parent, bg="#525561")

    # fixed design sizes (original used 1240x650)
    # The placements below assume the parent/frame will be sized accordingly

    # ================Background Image ====================
    try:
        Login_backgroundImage = PhotoImage(file="assets/image_1.png")
        bg_imageLogin = Label(frame, image=Login_backgroundImage, bg="#525561")
        bg_imageLogin.image = Login_backgroundImage
    except Exception:
        # fallback: plain background label
        bg_imageLogin = Label(frame, bg="#525561")

    bg_imageLogin.place(x=120, y=28)

    # ================ Header Text Left ====================
    try:
        Login_headerText_image_left = PhotoImage(file="assets/headerText_image.png")
        Login_headerText_image_label1 = Label(bg_imageLogin, image=Login_headerText_image_left, bg="#272A37")
        Login_headerText_image_label1.image = Login_headerText_image_left
        Login_headerText_image_label1.place(x=60, y=45)
    except Exception:
        pass

    Login_headerText1 = Label(bg_imageLogin, text="Electric Bill Calculator", fg="#FFFFFF",
                              font=("yu gothic ui bold", 20 * -1), bg="#272A37")
    Login_headerText1.place(x=110, y=45)

    # ================ Header Text Right ====================
    try:
        Login_headerText_image_right = PhotoImage(file="assets/headerText_image.png")
        Login_headerText_image_label2 = Label(bg_imageLogin, image=Login_headerText_image_right, bg="#272A37")
        Login_headerText_image_label2.image = Login_headerText_image_right
        Login_headerText_image_label2.place(x=400, y=45)
    except Exception:
        pass

    Login_headerText2 = Label(bg_imageLogin, anchor="nw", text="CS1C Final PIT", fg="#FFFFFF",
                              font=("yu gothic ui Bold", 20 * -1), bg="#272A37")
    Login_headerText2.place(x=450, y=45)

    # ================ LOGIN TO ACCOUNT HEADER ====================
    loginAccount_header = Label(bg_imageLogin, text="Login to continue", fg="#FFFFFF",
                                font=("yu gothic ui Bold", 28 * -1), bg="#272A37")
    loginAccount_header.place(x=75, y=121)

    # ================ NOT A MEMBER TEXT ====================
    loginText = Label(bg_imageLogin, text="Not a member yet?", fg="#FFFFFF",
                      font=("yu gothic ui Regular", 15 * -1), bg="#272A37")
    loginText.place(x=75, y=187)

    # ================ GO TO SIGN UP ====================
    switchSignup = Button(bg_imageLogin, text="Sign Up", fg="#206DB4",
                          font=("yu gothic ui Bold", 15 * -1), bg="#272A37", bd=0,
                          cursor="hand2", activebackground="#272A37", activeforeground="#ffffff",
                          command=(on_login_success if on_show_register is None else on_show_register))
    switchSignup.place(x=220, y=185, width=70, height=35)

    # ================ Email Name Section ====================
    try:
        Login_emailName_image = PhotoImage(file="assets/email.png")
        Login_emailName_image_Label = Label(bg_imageLogin, image=Login_emailName_image, bg="#272A37")
        Login_emailName_image_Label.image = Login_emailName_image
    except Exception:
        Login_emailName_image_Label = Label(bg_imageLogin, bg="#272A37")

    Login_emailName_image_Label.place(x=76, y=242)

    Login_emailName_text = Label(Login_emailName_image_Label, text="Email account", fg="#FFFFFF",
                                font=("yu gothic ui SemiBold", 13 * -1), bg="#3D404B")
    Login_emailName_text.place(x=25, y=0)

    try:
        Login_emailName_icon = PhotoImage(file="assets/email-icon.png")
        Login_emailName_icon_Label = Label(Login_emailName_image_Label, image=Login_emailName_icon, bg="#3D404B")
        Login_emailName_icon_Label.image = Login_emailName_icon
        Login_emailName_icon_Label.place(x=370, y=15)
    except Exception:
        pass

    Login_emailName_entry = Entry(Login_emailName_image_Label, bd=0, bg="#3D404B", highlightthickness=0,
                                  font=("yu gothic ui SemiBold", 16 * -1))
    Login_emailName_entry.place(x=8, y=17, width=354, height=27)

    # ================ Password Name Section ====================
    try:
        Login_passwordName_image = PhotoImage(file="assets/email.png")
        Login_passwordName_image_Label = Label(bg_imageLogin, image=Login_passwordName_image, bg="#272A37")
        Login_passwordName_image_Label.image = Login_passwordName_image
    except Exception:
        Login_passwordName_image_Label = Label(bg_imageLogin, bg="#272A37")

    Login_passwordName_image_Label.place(x=80, y=330)

    Login_passwordName_text = Label(Login_passwordName_image_Label, text="Password", fg="#FFFFFF",
                                   font=("yu gothic ui SemiBold", 13 * -1), bg="#3D404B")
    Login_passwordName_text.place(x=25, y=0)

    try:
        Login_passwordName_icon = PhotoImage(file="assets/pass-icon.png")
        Login_passwordName_icon_Label = Label(Login_passwordName_image_Label, image=Login_passwordName_icon, bg="#3D404B")
        Login_passwordName_icon_Label.image = Login_passwordName_icon
        Login_passwordName_icon_Label.place(x=370, y=15)
    except Exception:
        pass

    Login_passwordName_entry = Entry(Login_passwordName_image_Label, bd=0, bg="#3D404B", highlightthickness=0,
                                     font=("yu gothic ui SemiBold", 16 * -1))
    Login_passwordName_entry.place(x=8, y=17, width=354, height=27)

    # =============== Submit Button ====================
    try:
        Login_button_image_1 = PhotoImage(file="assets/button_1.png")
        Login_button_1 = Button(bg_imageLogin, image=Login_button_image_1, borderwidth=0, highlightthickness=0,
                                relief="flat", activebackground="#272A37", cursor="hand2")
        Login_button_1.image = Login_button_image_1
    except Exception:
        Login_button_1 = Button(bg_imageLogin, text="Login", bg="#206DB4", fg="#FFFFFF")

    Login_button_1.place(x=120, y=445, width=333, height=65)

    # ================ Header Text Down ====================
    try:
        Login_headerText_image_down = PhotoImage(file="assets/headerText_image.png")
        Login_headerText_image_label3 = Label(bg_imageLogin, image=Login_headerText_image_down, bg="#272A37")
        Login_headerText_image_label3.image = Login_headerText_image_down
        Login_headerText_image_label3.place(x=650, y=530)
    except Exception:
        pass

    Login_headerText3 = Label(bg_imageLogin, text="Luke Ezekiel B. abad", fg="#FFFFFF",
                              font=("yu gothic ui bold", 20 * -1), bg="#272A37")
    Login_headerText3.place(x=700, y=530)

    # ================ Forgot Password ====================
    def forgot_password():
        win = Toplevel()
        window_width = 350
        window_height = 350
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        position_top = int(screen_height / 4 - window_height / 4)
        position_right = int(screen_width / 2 - window_width / 2)
        win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        win.title('Forgot Password')
        win.configure(background='#272A37')
        win.resizable(False, False)

        email_entry3 = Entry(win, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1, bd=0)
        email_entry3.place(x=40, y=80, width=256, height=50)
        email_entry3.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
        email_label3 = Label(win, text='• Email', fg="#FFFFFF", bg='#272A37', font=("yu gothic ui", 11, 'bold'))
        email_label3.place(x=40, y=50)

        new_password_entry = Entry(win, bg="#3D404B", font=("yu gothic ui semibold", 12), show='•', highlightthickness=1, bd=0)
        new_password_entry.place(x=40, y=180, width=256, height=50)
        new_password_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
        new_password_label = Label(win, text='• New Password', fg="#FFFFFF", bg='#272A37', font=("yu gothic ui", 11, 'bold'))
        new_password_label.place(x=40, y=150)

        update_pass = Button(win, fg='#f8f8f8', text='Update Password', bg='#1D90F5', font=("yu gothic ui", 12, "bold"), cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5")
        update_pass.place(x=40, y=260, width=256, height=45)

    forgotPassword = Button(bg_imageLogin, text="Forgot Password", fg="#206DB4", font=("yu gothic ui Bold", 15 * -1), bg="#272A37", bd=0, activebackground="#272A37", activeforeground="#ffffff", cursor="hand2", command=forgot_password)
    forgotPassword.place(x=210, y=400, width=150, height=35)

    return frame


if __name__ == "__main__":
    # Standalone behaviour: create root window sized like original
    window = Tk()
    height = 650
    width = 1240
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 4) - (height // 4)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    window.configure(bg="#525561")

    frm = build_login_frame(window, 'Database/AccountSystem.db')
    frm.pack(fill='both', expand=True)
    window.resizable(False, False)
    window.mainloop()
from tkinter import *

window = Tk()

height = 650
width = 1240
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 4) - (height // 4)
window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

window.configure(bg="#525561")

# ================Background Image ====================
Login_backgroundImage = PhotoImage(file="assets/image_1.png")
bg_imageLogin = Label(
    window,
    image=Login_backgroundImage,
    bg="#525561"
)
bg_imageLogin.place(x=120, y=28)

# ================ Header Text Left ====================
Login_headerText_image_left = PhotoImage(file="assets/headerText_image.png")
Login_headerText_image_label1 = Label(
    bg_imageLogin,
    image=Login_headerText_image_left,
    bg="#272A37"
)
Login_headerText_image_label1.place(x=60, y=45)

Login_headerText1 = Label(
    bg_imageLogin,
    text="Electric Bill Calculator",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
Login_headerText1.place(x=110, y=45)

# ================ Header Text Right ====================
Login_headerText_image_right = PhotoImage(file="assets/headerText_image.png")
Login_headerText_image_label2 = Label(
    bg_imageLogin,
    image=Login_headerText_image_right,
    bg="#272A37"
)
Login_headerText_image_label2.place(x=400, y=45)

Login_headerText2 = Label(
    bg_imageLogin,
    anchor="nw",
    text="CS1C Final PIT",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 20 * -1),
    bg="#272A37"
)
Login_headerText2.place(x=450, y=45)

# ================ LOGIN TO ACCOUNT HEADER ====================
loginAccount_header = Label(
    bg_imageLogin,
    text="Login to continue",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#272A37"
)
loginAccount_header.place(x=75, y=121)

# ================ NOT A MEMBER TEXT ====================
loginText = Label(
    bg_imageLogin,
    text="Not a member yet?",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#272A37"
)
loginText.place(x=75, y=187)

# ================ GO TO SIGN UP ====================
switchSignup = Button(
    bg_imageLogin,
    text="Sign Up",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff"
)
switchSignup.place(x=220, y=185, width=70, height=35)


# ================ Email Name Section ====================
Login_emailName_image = PhotoImage(file="assets/email.png")
Login_emailName_image_Label = Label(
    bg_imageLogin,
    image=Login_emailName_image,
    bg="#272A37"
)
Login_emailName_image_Label.place(x=76, y=242)

Login_emailName_text = Label(
    Login_emailName_image_Label,
    text="Email account",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
Login_emailName_text.place(x=25, y=0)

Login_emailName_icon = PhotoImage(file="assets/email-icon.png")
Login_emailName_icon_Label = Label(
    Login_emailName_image_Label,
    image=Login_emailName_icon,
    bg="#3D404B"
)
Login_emailName_icon_Label.place(x=370, y=15)

Login_emailName_entry = Entry(
    Login_emailName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
)
Login_emailName_entry.place(x=8, y=17, width=354, height=27)


# ================ Password Name Section ====================
Login_passwordName_image = PhotoImage(file="assets/email.png")
Login_passwordName_image_Label = Label(
    bg_imageLogin,
    image=Login_passwordName_image,
    bg="#272A37"
)
Login_passwordName_image_Label.place(x=80, y=330)

Login_passwordName_text = Label(
    Login_passwordName_image_Label,
    text="Password",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
Login_passwordName_text.place(x=25, y=0)

Login_passwordName_icon = PhotoImage(file="assets/pass-icon.png")
Login_passwordName_icon_Label = Label(
    Login_passwordName_image_Label,
    image=Login_passwordName_icon,
    bg="#3D404B"
)
Login_passwordName_icon_Label.place(x=370, y=15)

Login_passwordName_entry = Entry(
    Login_passwordName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
)
Login_passwordName_entry.place(x=8, y=17, width=354, height=27)

# =============== Submit Button ====================
Login_button_image_1 = PhotoImage(
    file="assets/button_1.png")
Login_button_1 = Button(
    bg_imageLogin,
    image=Login_button_image_1,
    borderwidth=0,
    highlightthickness=0,
    # command=lambda:,
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
)
Login_button_1.place(x=120, y=445, width=333, height=65)

# ================ Header Text Down ====================
Login_headerText_image_down = PhotoImage(file="assets/headerText_image.png")
Login_headerText_image_label3 = Label(
    bg_imageLogin,
    image=Login_headerText_image_down,
    bg="#272A37"
)
Login_headerText_image_label3.place(x=650, y=530)

Login_headerText3 = Label(
    bg_imageLogin,
    text="Luke Ezekiel B. abad",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
Login_headerText3.place(x=700, y=530)

# ================ Forgot Password ====================
forgotPassword = Button(
    bg_imageLogin,
    text="Forgot Password",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    activebackground="#272A37",
    activeforeground="#ffffff",
    cursor="hand2",
    command=lambda: forgot_password(),
)
forgotPassword.place(x=210, y=400, width=150, height=35)


def forgot_password():

    win = Toplevel()
    window_width = 350
    window_height = 350
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    position_top = int(screen_height / 4 - window_height / 4)
    position_right = int(screen_width / 2 - window_width / 2)
    win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    win.title('Forgot Password')
    # win.iconbitmap('images/aa.ico')
    win.configure(background='#272A37')
    win.resizable(False, False)

    # ====== Email ====================
    email_entry3 = Entry(win, bg="#3D404B", font=("yu gothic ui semibold", 12), highlightthickness=1,
                         bd=0)
    email_entry3.place(x=40, y=80, width=256, height=50)
    email_entry3.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
    email_label3 = Label(win, text='• Email', fg="#FFFFFF", bg='#272A37',
                         font=("yu gothic ui", 11, 'bold'))
    email_label3.place(x=40, y=50)

    # ====  New Password ==================
    new_password_entry = Entry(win, bg="#3D404B", font=("yu gothic ui semibold", 12), show='•', highlightthickness=1,
                               bd=0)
    new_password_entry.place(x=40, y=180, width=256, height=50)
    new_password_entry.config(highlightbackground="#3D404B", highlightcolor="#206DB4")
    new_password_label = Label(win, text='• New Password', fg="#FFFFFF", bg='#272A37',
                               font=("yu gothic ui", 11, 'bold'))
    new_password_label.place(x=40, y=150)

    # ======= Update password Button ============
    update_pass = Button(win, fg='#f8f8f8', text='Update Password', bg='#1D90F5', font=("yu gothic ui", 12, "bold"),
                         cursor='hand2', relief="flat", bd=0, highlightthickness=0, activebackground="#1D90F5")
    update_pass.place(x=40, y=260, width=256, height=45)






window.resizable(False, False)
window.mainloop()
