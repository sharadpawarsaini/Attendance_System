import cv2  # type: ignore
import os
import pandas as pd  # type: ignore
from datetime import datetime
import qrcode  # type: ignore
from pyzbar.pyzbar import decode  # type: ignore
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

attendance_file = "C:/Users/DELL/Desktop/miniproject/attendance.xlsx"
qr_code_folder = "C:/Users/DELL/Desktop/miniproject/qr_codes"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

os.makedirs(qr_code_folder, exist_ok=True)

if not os.path.exists(attendance_file):
    attendance_df = pd.DataFrame(columns=["Student_ID", "Name", "Status", "Date"])
    attendance_df.to_excel(attendance_file, index=False)
else:
    attendance_df = pd.read_excel(attendance_file)

students = []

def add_student():
    student_id = student_id_entry.get()
    student_name = student_name_entry.get()
    if not student_id or not student_name:
        messagebox.showerror("Error", "Please enter both ID and Name")
        return
    students.append({"id": student_id, "name": student_name})
    student_listbox.insert(tk.END, f"{student_id} - {student_name}")
    generate_qr_code(student_id, student_name)
    student_id_entry.delete(0, tk.END)
    student_name_entry.delete(0, tk.END)

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
    global attendance_df
    current_date = datetime.now().strftime("%Y-%m-%d")
    existing_entry = attendance_df[(attendance_df['Student_ID'] == student_id) & (attendance_df['Date'] == current_date)]
    if existing_entry.empty:
        new_entry = pd.DataFrame({
            "Student_ID": [student_id],
            "Name": [student_name],
            "Status": ["Present"],
            "Date": [current_date]
        })
        attendance_df = pd.concat([attendance_df, new_entry], ignore_index=True)
        attendance_df.to_excel(attendance_file, index=False)
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

app = tk.Tk()
app.title("QR Code Attendance System")
app.geometry("700x700")
app.configure(bg="#2C3E50")

# Load background image
bg_image_path = "C:/Users/DELL/Desktop/miniproject/gehu_bg.jpg"
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((700, 700), Image.LANCZOS)

# Add watermark
draw = ImageDraw.Draw(bg_image)
font = ImageFont.load_default()
text = "Sharad Pawar Saini"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
draw.text(((700 - text_width) / 2, 680), text, font=font, fill=(255, 255, 255))

bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(app, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

frame = ttk.Frame(app, padding=20, style="Card.TFrame")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

style = ttk.Style()
style.configure("Card.TFrame", background="white", relief="raised", borderwidth=3)
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12), background="white")

for widget in frame.winfo_children():
    widget.configure(background="white")

ttk.Label(frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
student_id_entry = ttk.Entry(frame)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Student Name:").grid(row=1, column=0, padx=5, pady=5)
student_name_entry = ttk.Entry(frame)
student_name_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(frame, text="Add Student", command=add_student).grid(row=2, column=0, columnspan=2, pady=10)

ttk.Button(frame, text="Scan QR Code", command=scan_qr_code).grid(row=3, column=0, columnspan=2, pady=10)

qr_label = tk.Label(frame, bg="white")
qr_label.grid(row=4, column=0, columnspan=2, pady=10)

student_listbox = tk.Listbox(frame, height=6, width=40)
student_listbox.grid(row=5, column=0, columnspan=2, pady=10)

ttk.Label(frame, text="Attendance Log:").grid(row=6, column=0, columnspan=2)
attendance_listbox = tk.Listbox(frame, height=6, width=40)
attendance_listbox.grid(row=7, column=0, columnspan=2, pady=10)

app.mainloop()