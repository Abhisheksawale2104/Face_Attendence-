import tkinter as tk
from tkinter import messagebox, ttk

import mysql.connector

from connection import MysqlConnection
from initialize_database import initialize_database


class AttendanceApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Face Attendance")
        self.root.geometry("560x360")
        self.root.minsize(480, 320)

        container = ttk.Frame(root, padding=24)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            container, text="Face Attendance", font=("Segoe UI", 20, "bold")
        ).pack(anchor=tk.W)
        ttk.Label(
            container,
            text="Manage attendance with a webcam-based face recognition workflow.",
            wraplength=480,
        ).pack(anchor=tk.W, pady=(8, 24))

        database_group = ttk.LabelFrame(
            container, text="Database", padding=16
        )
        database_group.pack(fill=tk.X)

        self.database_status = tk.StringVar(value="Not checked")
        ttk.Label(database_group, text="Status:").grid(
            row=0, column=0, sticky=tk.W
        )
        ttk.Label(database_group, textvariable=self.database_status).grid(
            row=0, column=1, sticky=tk.W, padx=(8, 0)
        )

        actions = ttk.Frame(database_group)
        actions.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(16, 0))
        ttk.Button(
            actions, text="Check connection", command=self.check_connection
        ).pack(side=tk.LEFT)
        ttk.Button(
            actions, text="Initialize database", command=self.setup_database
        ).pack(side=tk.LEFT, padx=(8, 0))

        ttk.Label(
            container,
            text="Next: register people, capture face data, and record attendance.",
            wraplength=480,
        ).pack(anchor=tk.W, pady=(24, 0))

    def check_connection(self) -> None:
        try:
            with MysqlConnection() as database:
                database.read("SELECT 1")
        except (mysql.connector.Error, ValueError) as error:
            self.database_status.set("Connection failed")
            messagebox.showerror(
                "Database connection failed", str(error), parent=self.root
            )
            return

        self.database_status.set("Connected")
        messagebox.showinfo(
            "Database connection", "The attendance database is reachable.",
            parent=self.root,
        )

    def setup_database(self) -> None:
        try:
            initialize_database()
        except (mysql.connector.Error, OSError, ValueError) as error:
            self.database_status.set("Initialization failed")
            messagebox.showerror(
                "Database initialization failed", str(error), parent=self.root
            )
            return

        self.database_status.set("Ready")
        messagebox.showinfo(
            "Database initialized",
            "The attendance database and required tables are ready.",
            parent=self.root,
        )


def main() -> None:
    root = tk.Tk()
    AttendanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()