import cv2  # type: ignore
import os
import sqlite3
from datetime import datetime
import qrcode  # type: ignore
from pyzbar.pyzbar import decode  # type: ignore
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont # type: ignore

# Database Setup
db_path = "C:/Users/DELL/Desktop/miniproject/attendance.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    student_id TEXT,
    name TEXT,
    status TEXT,
    date TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

conn.commit()

# File Paths
qr_code_folder = "C:/Users/DELL/Desktop/miniproject/qr_codes"
bg_image_path = "C:/Users/DELL/Desktop/miniproject/gehu_bg.jpg"
os.makedirs(qr_code_folder, exist_ok=True)

def add_student():
    student_id = student_id_entry.get()
    student_name = student_name_entry.get()
    if not student_id or not student_name:
        messagebox.showerror("Error", "Please enter both ID and Name")
        return
    
    try:
        cursor.execute("INSERT INTO students (id, name) VALUES (?, ?)", (student_id, student_name))
        conn.commit()
        student_listbox.insert(tk.END, f"{student_id} - {student_name}")
        generate_qr_code(student_id, student_name)
        student_id_entry.delete(0, tk.END)
        student_name_entry.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists!")

def generate_qr_code(student_id, student_name):
    qr_data = f"{student_id} - {student_name}"
    qr = qrcode.make(qr_data)
    qr_path = os.path.join(qr_code_folder, f"{student_id}_qrcode.png")
    qr.save(qr_path)
    display_qr_code(qr_path)

def display_qr_code(qr_path):
    qr_img = Image.open(qr_path)
    qr_img = qr_img.resize((150, 150), Image.LANCZOS)
    qr_photo = ImageTk.PhotoImage(qr_img)
    qr_label.config(image=qr_photo)
    qr_label.image = qr_photo

def mark_attendance(student_id, student_name):
    current_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM attendance WHERE student_id = ? AND date = ?", (student_id, current_date))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO attendance (student_id, name, status, date) VALUES (?, ?, ?, ?)",
                       (student_id, student_name, "Present", current_date))
        conn.commit()
        attendance_listbox.insert(tk.END, f"{student_name} marked present.")

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Unable to read from the webcam.")
            break
        
        qr_codes = decode(frame)
        for qr in qr_codes:
            data = qr.data.decode("utf-8")
            student_id, student_name = data.split(" - ")
            mark_attendance(student_id, student_name)
            cap.release()
            cv2.destroyAllWindows()
            return

        cv2.imshow("QR Scanner", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

# Initialize GUI
app = tk.Tk()
app.title("GEHU ATTENDANCE SYSTEM")
app.state("zoomed")  # Set full-screen mode

# Load background image
bg_image = Image.open(bg_image_path).resize((1920, 1080), Image.LANCZOS)

# Add watermark
draw = ImageDraw.Draw(bg_image)
font = ImageFont.load_default()
text = "SHARAD PAWAR SAINI"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
draw.text(((1920 - text_width) / 2, 1060), text, font=font, fill=(255, 255, 255))

bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(app, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Title Label
title_label = tk.Label(app, text="GEHU ATTENDANCE SYSTEM", font=("Arial", 24, "bold"), fg="white", bg="#2C3E50")
title_label.pack(pady=20)

# Translucent Frame
frame = tk.Frame(app, bg="#ffffff", bd=5, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Form Fields
tk.Label(frame, text="Student ID:", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=5, pady=5)
student_id_entry = tk.Entry(frame, font=("Arial", 12))
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Student Name:", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=5, pady=5)
student_name_entry = tk.Entry(frame, font=("Arial", 12))
student_name_entry.grid(row=1, column=1, padx=5, pady=5)

# Buttons
tk.Button(frame, text="Add Student", font=("Arial", 12, "bold"), command=add_student, bg="#1ABC9C", fg="white").grid(row=2, column=0, columnspan=2, pady=10)
tk.Button(frame, text="Scan QR Code", font=("Arial", 12, "bold"), command=scan_qr_code, bg="#3498DB", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

# QR Display
qr_label = tk.Label(frame, bg="white")
qr_label.grid(row=4, column=0, columnspan=2, pady=10)

# Student Listbox
student_listbox = tk.Listbox(frame, height=6, width=40)
student_listbox.grid(row=5, column=0, columnspan=2, pady=10)

# Attendance Log
tk.Label(frame, text="Attendance Log:", font=("Arial", 12), bg="white").grid(row=6, column=0, columnspan=2)
attendance_listbox = tk.Listbox(frame, height=6, width=40)
attendance_listbox.grid(row=7, column=0, columnspan=2, pady=10)

app.mainloop()

conn.close()
