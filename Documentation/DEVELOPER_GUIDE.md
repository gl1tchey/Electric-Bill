# Developer Guide - Electric Bill Modular System

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Module Reference](#module-reference)
3. [API Documentation](#api-documentation)
4. [Usage Examples](#usage-examples)
5. [Extending the System](#extending-the-system)
6. [Troubleshooting](#troubleshooting)

## Architecture Overview

### Core Design
The system follows a **composite pattern** where:
- Each UI component is a self-contained, reusable frame builder
- Database operations are centralized in `db_utils`
- An orchestrator (`accountsystem.py`) composes components at runtime
- Components communicate via callbacks to maintain loose coupling

### Flow Diagram
```
┌─────────────────────────────────┐
│   accountsystem.main()          │
│   (Orchestrator)                │
└────────────────┬────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌──────────────┐
│Register │ │ Login   │ │ Billing      │
│Frame    │ │ Frame   │ │ Calculator   │
└────┬────┘ └────┬────┘ └──────┬───────┘
     │           │             │
     └───────────┼─────────────┘
                 │
                 ▼
         ┌──────────────────┐
         │  db_utils.py     │
         │  Database Ops    │
         └──────────────────┘
```

## Module Reference

### `accountsystem.py` - Main Orchestrator

**Purpose**: Entry point that composes and coordinates all UI components

**Entry Point**:
```python
from accountsystem import main
main()  # Launches the full application
```

**Key Function**: `main()`
- Creates root Tk window
- Initializes database
- Builds register and login frames
- Manages frame switching
- Handles login success (opens main app)

**Key Callback**: `on_login_success()`
```python
def on_login_success():
    root.destroy()
    open_main_app()
```

**Usage Pattern**:
```python
# Development/Testing
if __name__ == "__main__":
    main()
```

---

### `register_page.py` - Registration Module

**Purpose**: Provides user registration interface as a reusable Frame

**Main Function**:
```python
def build_register_frame(parent, db_path, on_show_login=None):
    """
    Build a registration frame.
    
    Args:
        parent: Parent tkinter widget (Frame or Tk)
        db_path: Path to SQLite database file
        on_show_login: Callback function to show login screen
        
    Returns:
        tkinter.Frame: Configured frame ready to pack()
    """
```

**Internal Callback**: `signup()`
- Validates input fields (no empty values, passwords match)
- Calls `db_utils.create_account()`
- Clears form on success
- Shows messagebox on error

**Example Usage**:
```python
# Standalone mode (development)
python register_page.py

# Embedded mode (production)
from register_page import build_register_frame
frame = build_register_frame(root, "app.db", on_show_login=switch_to_login)
frame.pack(fill='both', expand=True)
```

---

### `login_page.py` - Authentication Module

**Purpose**: Provides user login and password recovery interface

**Main Function**:
```python
def build_login_frame(parent, db_path, on_login_success=None):
    """
    Build a login frame.
    
    Args:
        parent: Parent tkinter widget (Frame or Tk)
        db_path: Path to SQLite database file
        on_login_success: Callback function when login succeeds
        
    Returns:
        tkinter.Frame: Configured frame ready to pack()
    """
```

**Internal Functions**:
- `login()` - Validates credentials via `db_utils.verify_user()`
- `forgot_password_dialog()` - Opens password recovery dialog
- `change_password()` - Updates password via `db_utils.update_password()`

**Features**:
- Forgot password functionality
- Password visibility toggle
- Error handling and user feedback

**Example Usage**:
```python
from login_page import build_login_frame

def on_success():
    print("User logged in!")

frame = build_login_frame(root, "app.db", on_login_success=on_success)
frame.pack(fill='both', expand=True)
```

---

### `electric_bill_gui.py` - Billing Calculator Module

**Purpose**: Main application for bill calculation and PDF generation

**Utility Functions**:
```python
def tiered(u, tiers):
    """Apply tiered pricing structure."""

def calculate_bill(units, customer_type):
    """Calculate bill with all charges (fixed, energy, VAT, env fee)."""

def open_main_app(parent=None):
    """
    Open the billing calculator interface.
    
    Args:
        parent: Parent tkinter widget (Tk or Toplevel)
                None = create standalone Tk window
                Provided = create Toplevel window
    """
```

**Dual Mode Operation**:
```python
# Standalone Mode
open_main_app()  # Creates Tk, runs mainloop

# Orchestrated Mode
open_main_app(parent=root)  # Creates Toplevel, returns
```

**Example Usage**:
```python
# As standalone application
python electric_bill_gui.py

# From orchestrator
from electric_bill_gui import open_main_app
open_main_app(parent=account_root)
```

---

### `Database/db_utils.py` - Database Operations

**Purpose**: Centralized database interface with account management

**Functions**:

#### `ensure_table(conn)`
```python
def ensure_table(conn):
    """Create accounts table if it doesn't exist."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
```

#### `create_account(conn, first, last, email, password)`
```python
def create_account(conn, first, last, email, password):
    """
    Create a new user account.
    
    Args:
        conn: sqlite3 connection
        first: First name
        last: Last name
        email: Email address (unique)
        password: Password (plain text - consider hashing)
        
    Returns:
        None
        
    Raises:
        sqlite3.IntegrityError: If email already exists
    """
```

#### `verify_user(conn, email, password)`
```python
def verify_user(conn, email, password):
    """
    Verify user credentials.
    
    Args:
        conn: sqlite3 connection
        email: User email
        password: User password
        
    Returns:
        bool: True if credentials match, False otherwise
    """
```

#### `user_exists(conn, email)`
```python
def user_exists(conn, email):
    """
    Check if user account exists.
    
    Args:
        conn: sqlite3 connection
        email: User email
        
    Returns:
        bool: True if user exists, False otherwise
    """
```

#### `update_password(conn, email, new_password)`
```python
def update_password(conn, email, new_password):
    """
    Update user password.
    
    Args:
        conn: sqlite3 connection
        email: User email
        new_password: New password (plain text)
        
    Returns:
        None
    """
```

**Example Usage**:
```python
import sqlite3
from Database import db_utils

conn = sqlite3.connect("app.db")

# Setup
db_utils.ensure_table(conn)

# Create account
db_utils.create_account(conn, "John", "Doe", "john@example.com", "pass123")

# Verify login
if db_utils.verify_user(conn, "john@example.com", "pass123"):
    print("Login successful!")

# Change password
db_utils.update_password(conn, "john@example.com", "newpass456")

conn.close()
```

## API Documentation

### Callback Signatures

#### `on_show_login`
Called when user wants to switch from register to login screen.
```python
def on_show_login():
    # Switch displayed frame
    login_frame.tkraise()
```

#### `on_login_success`
Called when user successfully authenticates.
```python
def on_login_success():
    # Close account window and open main app
    root.destroy()
    open_main_app()
```

### Frame Packing

All frame builders return tkinter.Frame objects that must be packed/placed:

```python
# Method 1: pack()
frame = build_register_frame(root, db_path, on_show_login)
frame.pack(fill='both', expand=True)

# Method 2: place()
frame = build_login_frame(root, db_path)
frame.place(x=0, y=0, width=1240, height=650)

# Method 3: grid()
frame = build_register_frame(root, db_path)
frame.grid(row=0, column=0, sticky="nsew")
```

## Usage Examples

### Example 1: Basic Orchestration
```python
from tkinter import Tk
from accountsystem import main

if __name__ == "__main__":
    main()
```

### Example 2: Embedded in Custom Window
```python
from tkinter import Tk, Frame
from register_page import build_register_frame
from login_page import build_login_frame

root = Tk()
root.title("My App")

# Create container
container = Frame(root)
container.pack(side="top", fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Create frames
register_frame = build_register_frame(
    container, 
    "app.db",
    on_show_login=lambda: show_frame(login_frame)
)
login_frame = build_login_frame(
    container,
    "app.db",
    on_login_success=lambda: print("Success!")
)

# Pack in same location (stacked)
register_frame.grid(row=0, column=0, sticky="nsew")
login_frame.grid(row=0, column=0, sticky="nsew")

# Show register first
register_frame.tkraise()

root.mainloop()
```

### Example 3: Custom Integration
```python
from tkinter import Tk, Toplevel, Button
from electric_bill_gui import open_main_app
from login_page import build_login_frame

root = Tk()

def show_billing():
    # Opens billing calc as new window
    open_main_app(parent=root)

# Create login frame
login = build_login_frame(
    root,
    "app.db", 
    on_login_success=show_billing
)
login.pack(fill='both', expand=True)

root.mainloop()
```

## Extending the System

### Adding a New Module

1. **Create frame builder**:
```python
# my_feature.py
from tkinter import Frame, Label, Button

def build_my_frame(parent, db_path, on_done=None):
    frame = Frame(parent, bg="#525561")
    
    Label(frame, text="My Feature").pack()
    Button(frame, text="Done", command=on_done).pack()
    
    return frame
```

2. **Import and use**:
```python
from my_feature import build_my_frame

frame = build_my_frame(root, "app.db", on_done=lambda: print("Done!"))
frame.pack()
```

### Adding Database Operations

1. **Extend db_utils**:
```python
# Database/db_utils.py

def create_billing_record(conn, email, amount, date):
    """Create a billing record."""
    conn.execute('''
        INSERT INTO billing (email, amount, date)
        VALUES (?, ?, ?)
    ''', (email, amount, date))
    conn.commit()
```

2. **Use in application**:
```python
from Database import db_utils

db_utils.create_billing_record(conn, "john@example.com", 500.00, "2025-11-28")
```

## Troubleshooting

### Issue: "No module named 'tkcalendar'"
**Solution**: Install missing dependency
```bash
pip install tkcalendar
```

### Issue: "No module named 'reportlab'"
**Solution**: Install PDF generation library
```bash
pip install reportlab
```

### Issue: "database is locked"
**Solution**: Ensure connections are properly closed
```python
conn = sqlite3.connect("app.db")
try:
    # Do work
finally:
    conn.close()  # Always close
```

### Issue: Frame doesn't show
**Solution**: Ensure frame is packed/placed
```python
frame = build_register_frame(root, "app.db")
frame.pack(fill='both', expand=True)  # Don't forget this!
root.mainloop()  # Required for display
```

### Issue: Callbacks not working
**Solution**: Pass callable functions, not function calls
```python
# WRONG - calls function immediately
frame = build_login_frame(root, db_path, on_login_success=my_function())

# RIGHT - passes reference to function
frame = build_login_frame(root, db_path, on_login_success=my_function)

# Also RIGHT - lambda for parameters
frame = build_login_frame(root, db_path, on_login_success=lambda: my_function(arg))
```

---

**Version**: 2.0 (Modular)
**Last Updated**: November 28, 2025
