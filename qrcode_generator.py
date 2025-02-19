import qrcode # type: ignore
import os

# Folder where QR codes will be saved
qr_code_folder = "C:/Users/DELL/Desktop/miniproject/qr_codes"

# Ensure the QR code folder exists, create it if not
if not os.path.exists(qr_code_folder):
    os.makedirs(qr_code_folder)

# Function to add a new student to the list
def add_student():
    students = []
    while True:
        student_id = input("Enter student ID: ")
        student_name = input("Enter student Name: ")
        
        # Add the student to the list
        students.append({"id": student_id, "name": student_name})
        
        # Ask if user wants to add another student
        another = input("Do you want to add another student? (y/n): ")
        if another.lower() != 'y':
            break
    
    return students

# Function to generate QR codes for all students
def generate_qr_for_all_students(students):
    for student in students:
        student_id = student["id"]
        student_name = student["name"]
        
        # Create QR code data
        qr_data = f"{student_id} - {student_name}"
        
        # Generate the QR code
        qr = qrcode.make(qr_data)
        
        # Save the QR code image in the folder
        qr_path = os.path.join(qr_code_folder, f"{student_id}_qrcode.png")
        qr.save(qr_path)
        
        # Output message for each generated QR code
        print(f"Generated QR code for {student_name} at {qr_path}")

# Main function
if __name__ == "__main__":
    # Get student data from user input
    students = add_student()
    
    # Generate QR codes for the students
    generate_qr_for_all_students(students)
