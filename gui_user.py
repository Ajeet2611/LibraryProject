import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from db import get_connection
from datetime import date
import os

# ================= PATH =================
BASE_DIR = os.path.dirname(__file__)
ASSETS = os.path.join(BASE_DIR, "assets")


def open_user_dashboard(user):
    username = user["Username"]
    institution_id = user["InstitutionID"]

    root = tk.Tk()
    root.title("User Dashboard")
    root.geometry("1050x600")
    root.resizable(False, False)

    # ================= BACKGROUND =================
    bg = ImageTk.PhotoImage(
        Image.open(os.path.join(ASSETS, "bg.jpg")).resize((1050, 600))
    )
    tk.Label(root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    # ================= TITLE =================
    tk.Label(
        root,
        text=f"Welcome, {username}",
        font=("Arial", 22, "bold"),
        bg="black",
        fg="white"
    ).place(x=20, y=15)

    # ================= AVAILABLE BOOKS =================
    frame1 = tk.LabelFrame(
        root, text="Available Books",
        font=("Arial", 12, "bold"),
        padx=10, pady=10
    )
    frame1.place(x=20, y=80, width=500, height=420)

    cols1 = ("Title", "Author", "Available")
    tree_books = ttk.Treeview(frame1, columns=cols1, show="headings")
    tree_books.pack(fill="both", expand=True)

    for c in cols1:
        tree_books.heading(c, text=c)
        tree_books.column(c, width=150)

    def load_books():
        tree_books.delete(*tree_books.get_children())

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT Title, Author, AvailableCopies
            FROM Books
            WHERE InstitutionID=%s AND AvailableCopies>0
            """,
            (institution_id,)
        )
        for row in cur.fetchall():
            tree_books.insert("", "end", values=row)

        cur.close()
        conn.close()

    tk.Button(
        frame1, text="Refresh",
        bg="#2563eb", fg="white",
        command=load_books
    ).pack(pady=5)

    load_books()

    # ================= MY ISSUED BOOKS =================
    frame2 = tk.LabelFrame(
        root, text="My Issued Books",
        font=("Arial", 12, "bold"),
        padx=10, pady=10
    )
    frame2.place(x=540, y=80, width=480, height=420)

    cols2 = ("Title", "Issue Date", "Due Date", "Status", "Fine")
    tree_issue = ttk.Treeview(frame2, columns=cols2, show="headings")
    tree_issue.pack(fill="both", expand=True)

    for c in cols2:
        tree_issue.heading(c, text=c)
        tree_issue.column(c, width=90)

    def load_issued():
        tree_issue.delete(*tree_issue.get_children())

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT B.Title, T.IssueDate, T.DueDate, T.ReturnStatus
            FROM Transactions T
            JOIN Books B ON T.BookID = B.BookID
            JOIN Members M ON T.MemberID = M.MemberID
            WHERE M.Name=%s AND T.InstitutionID=%s
            """,
            (username, institution_id)
        )

        today = date.today()

        for r in cur.fetchall():
            fine = 0
            status = r[3]

            if status == "ISSUED" and today > r[2]:
                fine = (today - r[2]).days * 5
                tag = "late"
            else:
                tag = "ok"

            tree_issue.insert(
                "", "end",
                values=(r[0], r[1], r[2], status, f"₹{fine}"),
                tags=(tag,)
            )

        tree_issue.tag_configure("late", background="#fca5a5")
        tree_issue.tag_configure("ok", background="#bbf7d0")

        cur.close()
        conn.close()

    tk.Button(
        frame2, text="Refresh",
        bg="#16a34a", fg="white",
        command=load_issued
    ).pack(pady=5)

    load_issued()

    # ================= MESSAGE TO ADMIN =================
    frame3 = tk.LabelFrame(
        root, text="Message to Admin",
        font=("Arial", 12, "bold"),
        padx=10, pady=10
    )
    frame3.place(x=20, y=520, width=800, height=60)

    msg_entry = tk.Entry(frame3, width=90)
    msg_entry.pack(side="left", padx=10)

    def send_msg():
        msg = msg_entry.get().strip()
        if not msg:
            messagebox.showerror("Error", "Message cannot be empty")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO Messages
            (Username, Message, MessageDate, Status, InstitutionID)
            VALUES (%s, %s, CURDATE(), 'OPEN', %s)
            """,
            (username, msg, institution_id)
        )
        conn.commit()
        cur.close()
        conn.close()

        messagebox.showinfo("Sent", "Message sent to Admin")
        msg_entry.delete(0, tk.END)

    tk.Button(
        frame3, text="Send",
        bg="#f59e0b", fg="black",
        width=12, command=send_msg
    ).pack(side="left")

    # ================= LOGOUT =================
    tk.Button(
        root, text="Logout",
        bg="#dc2626", fg="white",
        width=15, font=("Arial", 11, "bold"),
        command=root.destroy
    ).place(x=860, y=525)

    root.mainloop()
