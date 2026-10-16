import json

FILE_NAME = "students.json"


def calculate_class_average():
    # Load student attendance data
    with open(FILE_NAME, "r") as file:
        data = json.load(file)

    student_percentages = []

    # Calculate each student's attendance percentage
    for student in data["students"]:
        attendance = student["attendance"]

        present_days = sum(
            1 for status in attendance.values()
            if status == "Present"
        )

        recorded_days = sum(
            1 for status in attendance.values()
            if status in ["Present", "Absent"]
        )

        if recorded_days > 0:
            percentage = (present_days / recorded_days) * 100
            student_percentages.append(percentage)

        print(
            f"{student['name']}: "
            f"{percentage:.2f}%"
            if recorded_days > 0
            else f"{student['name']}: No attendance recorded"
        )

    # Calculate class average
    if student_percentages:
        class_average = (
            sum(student_percentages) / len(student_percentages)
        )
    else:
        class_average = 0

    print(f"\nClass Average Attendance: {class_average:.2f}%")

    return round(class_average, 2)


if __name__ == "__main__":
    calculate_class_average()