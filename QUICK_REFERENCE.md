# Electric Bill Account System - Quick Reference

## File Structure & Purpose

```
Electric-Bill/
├── accountsystem.py           # Main orchestrator - composes all screens
├── electric_bill_gui.py       # Billing calculator module (refactored to return Frame)
├── register_page.py           # Registration UI module
├── login_page.py              # Login UI module (now with Sign Up button)
├── pdf_maker.py               # PDF generation for bills
├── Database/
│   ├── db_utils.py           # Database utility functions (5 functions)
│   ├── create_database.py     # Initial database setup
│   └── AccountSystem.db       # SQLite database
├── assets/                     # UI images/resources
├── README.md                   # Project documentation
├── UI_FLOW_IMPLEMENTATION.md  # This implementation guide
└── __pycache__/               # Python cache
```

## Module Signatures

### 1. `Database/db_utils.py`
```python
def ensure_table(conn):
    """Create AccountDB table if not exists"""

def create_account(conn, first_name, last_name, email, password):
    """Add new user account"""

def user_exists(conn, email):
    """Check if email already registered"""

def verify_user(conn, email, password):
    """Validate email/password combination"""

def update_password(conn, email, new_password):
    """Change user password"""
```

### 2. `register_page.py`
```python
def build_register_frame(parent, db_path, on_show_login=None, on_register_success=None):
    """
    Build registration UI frame
    
    Args:
        parent: Parent tkinter widget
        db_path: Path to database
        on_show_login: Callback when user clicks "Back to Login"
        on_register_success: Callback after successful registration
    
    Returns:
        tkinter.Frame
    """
```

### 3. `login_page.py`
```python
def build_login_frame(parent, db_path, on_login_success=None, on_show_register=None):
    """
    Build login UI frame
    
    Args:
        parent: Parent tkinter widget
        db_path: Path to database
        on_login_success: Callback after successful login
        on_show_register: Callback when user clicks "Sign Up"
    
    Returns:
        tkinter.Frame
    """
```

### 4. `electric_bill_gui.py`
```python
def calculate_bill(units, customer_type):
    """
    Calculate electric bill
    
    Args:
        units: kWh consumed
        customer_type: "residential" or "commercial"
    
    Returns:
        Tuple: (energy, fixed, vat, env_fee, applied_rates, total)
    """

def open_main_app(parent=None, on_logout=None):
    """
    Build billing calculator UI frame
    
    Args:
        parent: Parent tkinter widget (None = standalone mode)
        on_logout: Callback when user clicks logout
    
    Returns:
        tkinter.Frame
    """
```

## Frame Navigation Pattern

```
accountsystem.py main():
    root = Tk()
    
    # Create 4 container frames
    sign_in = Frame(root)
    sign_up = Frame(root)
    success = Frame(root)
    account = Frame(root)
    
    # Stack them on top of each other
    for frame in (sign_in, sign_up, success, account):
        frame.grid(row=0, column=0, sticky="nsew")
    
    # Populate frames with UI
    reg_frame = build_register_frame(sign_up, ..., on_register_success=on_register_success)
    reg_frame.pack(fill='both', expand=True)
    
    login_frame = build_login_frame(sign_in, ..., on_show_register=on_show_register)
    login_frame.pack(fill='both', expand=True)
    
    account_frame = open_main_app(parent=account, on_logout=on_logout)
    account_frame.pack(fill='both', expand=True)
    
    # Show login by default
    show_frame(sign_in)
    
    root.mainloop()
```

## Callback Chain

```
Register Form
    → on_register_success() 
        → show_frame(success)
            → Button("Proceed to Login")
                → on_success_to_login()
                    → show_frame(sign_in)
                        → Button("Sign Up")
                            → on_show_register()
                                → show_frame(sign_up)

Login Form
    → on_login_success()
        → show_frame(account)
            → Billing Calculator
                → Button("Logout")
                    → on_logout()
                        → show_frame(sign_in)
```

## Key Features

### Database
- SQLite3 with prepared statements (SQL injection safe)
- Table: AccountDB (FirstName, LastName, Email, Password, id)
- 5 utility functions for all operations

### UI
- Tkinter with Frame-based modular design
- No circular imports
- Clean callback-based communication
- All screens in single window (no external popups except dialogs)
- Responsive layout

### Billing
- Tiered rate calculation for Residential and Commercial
- VAT (12%) and Environmental Fee (0.25%)
- Fixed monthly fee
- PDF generation support

### Security
- SQL injection prevention (prepared statements)
- Password operations via database utilities
- Email validation during registration
- Session isolation (one user at a time)

## Testing Commands

```bash
# Test database utilities
python Database/db_utils.py

# Test billing calculations  
python electric_bill_gui.py

# Run full account system
python accountsystem.py

# Test registration module
python register_page.py

# Test login module
python login_page.py
```

## UI Components

### Login Screen (sign_in)
- Email input field
- Password input field
- Login button
- Forgot Password button (opens dialog)
- Sign Up button (navigates to register)

### Register Screen (sign_up)
- First Name input
- Last Name input
- Email input
- Password input
- Sign Up button
- Back to Login button

### Success Screen (success)
- Congratulations message
- "Proceed to Login" button

### Account System (account)
- Customer Name input
- Account Number input
- Address input
- Customer Type dropdown
- Billing Month date picker
- kWh Used input
- Generate Bill button
- Download PDF button
- Logout button (red)
- Output text display

## Database Schema

```sql
CREATE TABLE AccountDB (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL
);
```

## Error Handling

- Empty field validation on forms
- Email format checking
- Duplicate email prevention
- Password mismatch handling
- Database connection error handling
- Invalid input handling in billing calculator
- PDF save dialog cancellation handling

## Performance Notes

- Database queries: O(1) lookups by email (indexed primary key)
- Frame switching: Instant (uses tkraise method)
- PDF generation: ~1-2 seconds (depends on file system)
- Memory: Minimal (single window, no retained dialogs)

## Known Limitations

- No image loading (assets folder empty in base)
- No network connectivity required (offline capable)
- Single user at a time (sequential login only)
- No user profile pictures
- No billing history tracking
- PDFs saved locally only (no cloud)

## Extension Points

To add new features:

1. **Add new screen**: Create frame container, frame builder, callback
2. **Add authentication**: Modify verify_user() in db_utils.py
3. **Add features to billing**: Update open_main_app() and calculate_bill()
4. **Add database fields**: Modify schema in db_utils.ensure_table()
5. **Add callbacks**: Create new callback functions in accountsystem.py main()
