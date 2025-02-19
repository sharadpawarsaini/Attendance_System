import pandas as pd # type: ignore
import os
# Path to the attendance file
attendance_file = "C:/Users/DELL/Desktop/miniproject/attendance.xlsx"

# Create a new attendance sheet if it doesn't exist
if not os.path.exists(attendance_file):
    df = pd.DataFrame(columns=["Student_ID", "Name", "Status", "Date"])
    df.to_excel(attendance_file, index=False)
