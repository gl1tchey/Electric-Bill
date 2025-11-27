"""Database helper utilities for account operations.

Provides simple wrappers around sqlite3 connection to create accounts,
verify credentials and update passwords.
"""
import sqlite3


def ensure_table(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS AccountDB (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT,
            LastName TEXT,
            Email TEXT UNIQUE, 
            Password TEXT
        )
        """
    )
    conn.commit()


def create_account(conn: sqlite3.Connection, first, last, email, password):
    ensure_table(conn)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO AccountDB (FirstName, LastName, Email, Password) VALUES (?, ?, ?, ?)",
        (first, last, email, password),
    )
    conn.commit()


def verify_user(conn: sqlite3.Connection, email, password) -> bool:
    ensure_table(conn)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM AccountDB WHERE Email = ? AND Password = ?", (email, password))
    return cur.fetchone() is not None


def user_exists(conn: sqlite3.Connection, email) -> bool:
    ensure_table(conn)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM AccountDB WHERE Email = ?", (email,))
    return cur.fetchone() is not None


def update_password(conn: sqlite3.Connection, email, new_password):
    ensure_table(conn)
    cur = conn.cursor()
    cur.execute("UPDATE AccountDB SET Password = ? WHERE Email = ?", (new_password, email))
    conn.commit()
