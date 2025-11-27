# Project File Structure & Descriptions

## Directory Tree

```
Electric-Bill/
│
├── accountsystem.py                    # MAIN ENTRY POINT
│   └─ Purpose: Orchestrates all UI screens (login, register, success, billing)
│   └─ Function: main() creates window and manages 4-frame navigation
│   └─ Size: ~91 lines
│
├── electric_bill_gui.py                # BILLING CALCULATOR MODULE
│   ├─ Purpose: Bill calculation and PDF generation
│   ├─ Functions:
│   │  ├─ calculate_bill(units, customer_type) → bill details
│   │  ├─ tiered(u, tiers) → cost calculation with tiers
│   │  └─ open_main_app(parent, on_logout) → Frame
│   ├─ Features:
│   │  ├─ Residential and Commercial rates
│   │  ├─ VAT and environmental fees
│   │  ├─ PDF generation
│   │  └─ Logout callback
│   └─ Size: ~203 lines
│
├── login_page.py                       # LOGIN MODULE
│   ├─ Purpose: User authentication UI
│   ├─ Function: build_login_frame(parent, db_path, on_login_success, on_show_register) → Frame
│   ├─ Features:
│   │  ├─ Email/password entry
│   │  ├─ Forgot password dialog
│   │  ├─ Sign Up button (NEW)
│   │  └─ Database validation
│   └─ Size: ~140 lines
│
├── register_page.py                    # REGISTRATION MODULE
│   ├─ Purpose: New account creation UI
│   ├─ Function: build_register_frame(parent, db_path, on_show_login, on_register_success) → Frame
│   ├─ Features:
│   │  ├─ Name/email/password entry
│   │  ├─ Form validation
│   │  ├─ Duplicate email check
│   │  ├─ Success callback (NEW)
│   │  └─ Back to login button
│   └─ Size: ~129 lines
│
├── pdf_maker.py                        # PDF GENERATION UTILITY
│   ├─ Purpose: Generate PDF bills
│   ├─ Function: generate_bill_pdf(data, output_file)
│   ├─ Features:
│   │  ├─ ReportLab PDF generation
│   │  └─ Formatted bill layout
│   └─ Size: ~30-50 lines (approximate)
│
├── Database/                           # DATABASE MODULE
│   ├─ __init__.py                     # Package initializer
│   ├─ db_utils.py                     # DATABASE UTILITIES
│   │  ├─ Purpose: All database operations
│   │  ├─ Functions:
│   │  │  ├─ ensure_table(conn) → creates table
│   │  │  ├─ create_account(conn, fname, lname, email, pwd) → adds user
│   │  │  ├─ user_exists(conn, email) → bool
│   │  │  ├─ verify_user(conn, email, pwd) → bool
│   │  │  └─ update_password(conn, email, new_pwd) → updates password
│   │  ├─ Features:
│   │  │  ├─ SQL injection prevention
│   │  │  ├─ Prepared statements
│   │  │  └─ Hash-based storage (when implemented)
│   │  └─ Size: ~70 lines
│   │
│   ├─ create_database.py               # INITIAL SETUP (rarely used)
│   │  └─ Purpose: Create database structure initially
│   │
│   └─ AccountSystem.db                 # SQLITE DATABASE FILE
│      └─ Table: AccountDB
│         ├─ Columns: id, FirstName, LastName, Email, Password
│         ├─ Indexed: Email (unique)
│         └─ Auto-created if missing
│
├── assets/                             # UI RESOURCES
│   └─ [contains background images and icons]
│
├── __pycache__/                        # PYTHON CACHE (auto-generated)
│
├── README.md                           # PROJECT README
│   └─ Original project documentation
│
├── UI_FLOW_IMPLEMENTATION.md           # IMPLEMENTATION GUIDE (NEW)
│   └─ Detailed explanation of UI flow changes
│
├── QUICK_REFERENCE.md                  # ARCHITECTURE REFERENCE (NEW)
│   └─ Module signatures and patterns
│
├── FINAL_VERIFICATION.md               # VERIFICATION REPORT (NEW)
│   └─ Testing results and feature verification
│
└── tutorial.txt                        # TUTORIAL (optional)
```

## Critical Files (Run These)

### To Run Full System
```bash
python accountsystem.py
```
**What happens:**
1. Opens main window (1240x650)
2. Shows login screen
3. Can register, login, or reset password
4. After login: Shows billing calculator
5. Can calculate bills, generate PDFs
6. Can logout to return to login

### To Run Just Billing App
```bash
python electric_bill_gui.py
```
**What happens:**
1. Opens billing calculator in standalone window
2. No login required
3. Can enter customer data and calculate bills

### To Test Database
```bash
python Database/db_utils.py
```
**What happens:**
1. Runs built-in tests
2. Creates test database
3. Verifies all database functions

### To Test Login
```bash
python login_page.py
```
**What happens:**
1. Opens login frame in standalone window
2. Can test login functionality

### To Test Register
```bash
python register_page.py
```
**What happens:**
1. Opens registration frame in standalone window
2. Can test registration functionality

## File Modifications (Recent)

### electric_bill_gui.py
- BEFORE: Created Tk/Toplevel, ran mainloop, returned None
- AFTER: Creates Frame, returns Frame, mainloop only if owns_root
- REASON: Must work with orchestrator pattern
- IMPACT: Now embeddable in accountsystem window

### accountsystem.py
- BEFORE: 2 frames (sign_in, sign_up), no success screen
- AFTER: 4 frames (sign_in, sign_up, success, account)
- REASON: User wants success screen after registration
- IMPACT: Better user experience, more navigation options

### login_page.py
- BEFORE: No way to go to registration from login
- AFTER: "Sign Up" button added
- REASON: Usability improvement
- IMPACT: Users can switch between login and register

### register_page.py
- BEFORE: No callback after successful registration
- AFTER: Calls on_register_success() callback
- REASON: Need to trigger success screen display
- IMPACT: Proper flow: Register → Success → Login

## Dependencies

### Installed Packages
```
tkinter         (built-in with Python)
sqlite3         (built-in with Python)
tkcalendar      (pip install tkcalendar)
reportlab       (pip install reportlab)
pandas          (optional, for data analysis)
```

### Python Version
- Minimum: Python 3.7
- Tested: Python 3.10
- Recommended: Python 3.10+

## Database Schema

```sql
CREATE TABLE AccountDB (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL
);

-- Indexes (created automatically)
-- PRIMARY KEY on id
-- UNIQUE constraint on Email
```

## Entry Points

### 1. Main Application
```bash
python accountsystem.py
→ Creates orchestrator window
→ Shows all 4 screens
→ Full user flow
```

### 2. Standalone Billing
```bash
python electric_bill_gui.py
→ Creates billing calculator window
→ No authentication
→ Quick billing calculations
```

### 3. Testing & Development
```bash
python login_page.py      # Test login UI
python register_page.py    # Test register UI
python Database/db_utils.py # Test database
```

## Code Statistics

| File | Lines | Purpose |
|------|-------|---------|
| accountsystem.py | 91 | Orchestrator |
| electric_bill_gui.py | 203 | Billing + UI |
| login_page.py | 140 | Login module |
| register_page.py | 129 | Registration module |
| Database/db_utils.py | 70 | Database utilities |
| pdf_maker.py | 40-50 | PDF generation |
| **Total** | **~670** | **Complete system** |

## Architecture Pattern

```
Tkinter Hierarchy:
├─ Tk (root window)
│  ├─ Frame (sign_in - contains login UI)
│  ├─ Frame (sign_up - contains register UI)
│  ├─ Frame (success - congratulations screen)
│  └─ Frame (account - contains billing UI)
│
Frames are stacked using grid() and raised using tkraise()

Communication:
├─ Callbacks between modules
├─ No global state
├─ Dependency injection via parameters
└─ Clean separation of concerns
```

## Workflow

```
User starts app
    ↓
accountsystem.py main() runs
    ↓
Tk window created + DB initialized
    ↓
4 Frames created and stacked
    ↓
Frame builders populate frames
    ↓
show_frame(sign_in) displays login
    ↓
User chooses path:
├─ Login path:
│  ├─ Enter email/password
│  ├─ Verify against database
│  ├─ If success: show_frame(account)
│  └─ Billing calculator displays
│
├─ Forgot password path:
│  ├─ Click "Forgot Password"
│  ├─ Dialog opens
│  ├─ Enter new password
│  └─ Return to login
│
└─ Register path:
   ├─ Click "Sign Up"
   ├─ show_frame(sign_up)
   ├─ Fill registration form
   ├─ Create account
   ├─ Success callback fires
   ├─ show_frame(success)
   ├─ See congratulations
   ├─ Click "Proceed to Login"
   └─ show_frame(sign_in)
```

## Configuration

### Database Path
```python
DB_PATH = "Database/AccountSystem.db"
```
Located in Database/ directory, created automatically

### Window Size
```python
width = 1240
height = 650
```
Centered on screen

### Window Title
```
"Electric Bill Account System"
```

### Billing Rates (Residential)
- Tier 1: 50 kWh @ 5.0/kWh
- Tier 2: 50 kWh @ 6.5/kWh
- Tier 3: 100 kWh @ 8.0/kWh
- Tier 4: unlimited @ 10.0/kWh
- Fixed: 40
- VAT: 12%
- Env Fee: 0.25%

### Billing Rates (Commercial)
- Tier 1: 100 kWh @ 3.5/kWh
- Tier 2: 200 kWh @ 5.0/kWh
- Tier 3: 500 kWh @ 6.5/kWh
- Tier 4: unlimited @ 7.5/kWh
- Fixed: 100
- VAT: 12%
- Env Fee: 0.25%

## Troubleshooting

### Database not creating?
```python
# Automatic solution:
# db_utils.ensure_table() creates it on first run
# Or manually:
python Database/db_utils.py
```

### Can't find modules?
```python
# Ensure you're in Electric-Bill/ directory:
cd "path/to/Electric-Bill"
python accountsystem.py
```

### Tkinter not found?
```bash
# Install tkinter (usually included with Python)
pip install tk
# Or on Linux:
apt-get install python3-tk
```

### Missing dependencies?
```bash
pip install tkcalendar reportlab pandas
```

## File Navigation Map

```
To understand the flow:
1. Start: read accountsystem.py (main orchestrator)
2. See what functions it calls from:
   - register_page.py (build_register_frame)
   - login_page.py (build_login_frame)
   - electric_bill_gui.py (open_main_app)
3. Database layer:
   - Database/db_utils.py (all DB operations)
4. PDF generation:
   - pdf_maker.py (generate_bill_pdf)

Dependencies flow:
accountsystem.py
├─ imports register_page.build_register_frame
├─ imports login_page.build_login_frame
├─ imports electric_bill_gui.open_main_app
├─ imports Database.db_utils
│  └─ imports sqlite3
├─ imports electric_bill_gui.calculate_bill
│  └─ imports pdf_maker.generate_bill_pdf
│     └─ imports reportlab
└─ imports tkinter (for Frames, Buttons, etc)
```

## Version History

- **v1.0**: Initial monolithic application
- **v2.0**: Modularized architecture with orchestrator (CURRENT)
  - Multi-screen navigation
  - Callback-based communication
  - Frame embedding pattern
  - Success screen added
  - Logout functionality added
  - Sign Up button added
