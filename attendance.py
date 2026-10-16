import json
from datetime import date

FILE_NAME = "students.json"


def load_data():
    """Load attendance data from the JSON file."""
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_data(data):
    """Save updated attendance data to the JSON file."""
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=2)


def find_student(data, roll_no):
    """Find a student using their roll number."""
    for student in data["students"]:
        if student["roll_no"] == str(roll_no):
            return student
    return None


def mark_attendance(roll_no, day, status):
    """Mark or update attendance for a particular date."""
    data = load_data()
    student = find_student(data, roll_no)

    if student is None:
        return {"success": False, "message": "Student not found"}

    # Check whether the date is valid
    try:
        date.fromisoformat(day)
    except ValueError:
        return {"success": False, "message": "Invalid date format"}

    if day not in student["attendance"]:
        return {
            "success": False,
            "message": "Date is not in the attendance records"
        }

    if status not in ["Present", "Absent"]:
        return {"success": False, "message": "Invalid status"}

    student["attendance"][day] = status
    save_data(data)

    return {
        "success": True,
        "message": f"Attendance updated for {student['name']}",
        "roll_no": str(roll_no),
        "date": day,
        "status": status
    }


def remove_attendance(roll_no, day):
    """Remove attendance for a particular date."""
    data = load_data()
    student = find_student(data, roll_no)

    if student is None:
        return {"success": False, "message": "Student not found"}

    if day not in student["attendance"]:
        return {
            "success": False,
            "message": "No attendance record exists for this date"
        }

    del student["attendance"][day]
    save_data(data)

    return {
        "success": True,
        "message": f"Attendance removed for {student['name']}",
        "roll_no": str(roll_no),
        "date": day
    }


def get_attendance(roll_no):
    """Calculate a student's attendance summary."""
    data = load_data()
    student = find_student(data, roll_no)

    if student is None:
        return {"success": False, "message": "Student not found"}

    attendance = student["attendance"]
    present = sum(
        1 for status in attendance.values()
        if status == "Present"
    )
    absent = sum(
        1 for status in attendance.values()
        if status == "Absent"
    )
    recorded_days = present + absent

    percentage = (
        (present / recorded_days) * 100
        if recorded_days > 0 else 0
    )

    return {
        "success": True,
        "name": student["name"],
        "roll_no": student["roll_no"],
        "present_days": present,
        "absent_days": absent,
        "recorded_days": recorded_days,
        "attendance_percentage": round(percentage, 2)
    }


# Test the tools
if __name__ == "__main__":
    result = get_attendance("101")
    print(json.dumps(result, indent=2))