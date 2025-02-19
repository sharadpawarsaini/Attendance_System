# Attendance_System
# **QR Code-Based Attendance System**  

## **Project Description**  

### **Introduction**  
The **QR Code-Based Attendance System** is a smart and efficient way to manage student attendance digitally. This system leverages **QR code technology** to mark attendance automatically, reducing manual effort and improving accuracy. It is designed using **Python with Tkinter for the GUI**, **OpenCV for QR scanning**, and **Pandas for attendance data storage**.  

### **Features**  
✅ **Student Registration**: Users can add student details (ID & Name) to the system.  
✅ **QR Code Generation**: The system generates and displays a **unique QR code** for each student.  
✅ **QR Code Scanning**: Uses a **webcam** to scan student QR codes and mark attendance automatically.  
✅ **Attendance Logging**: Stores attendance records in an **Excel file (attendance.xlsx)** with timestamps.  
✅ **User-Friendly GUI**: A **beautiful Tkinter-based interface** with a **background image, translucent form, and watermark**.  
✅ **Watermark Signature**: Displays **"SHARAD PAWAR SAINI"** at the bottom for authenticity.  

### **Technology Stack**  
- **Python** (Tkinter for GUI, OpenCV for QR scanning, Pandas for data storage)  
- **QR Code Library** (qrcode, pyzbar for generating and decoding QR codes)  
- **Pandas & Excel** (Stores attendance data in an Excel file)  
- **OpenCV** (Used for real-time QR code scanning via a webcam)  
- **PIL (Pillow)** (For handling images, adding a watermark)  

### **How It Works**  
1. **Student Registration**: Enter the student’s ID and Name → Click “Add Student.”  
2. **QR Code Generation**: A QR code is generated for the student and saved.  
3. **QR Code Display**: The QR is displayed in the GUI for reference.  
4. **Scanning for Attendance**: The student scans their QR code via the webcam.  
5. **Attendance Marking**: If the QR is valid, attendance is recorded in the Excel sheet.  
6. **Viewing Records**: The attendance log is displayed in the GUI.  

### **Project Benefits**  
📌 **Eliminates Manual Errors** – No need for paper-based attendance.  
📌 **Time-Efficient** – Fast and automated attendance marking.  
📌 **Secure & Reliable** – Ensures no unauthorized attendance.  
📌 **User-Friendly** – Simple interface with a modern look.  
