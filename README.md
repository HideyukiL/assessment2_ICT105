# assessment2_ICT105

# School Attendance System - Backend Database Module - Lucas Hideyuki

This module serves as the relational database engine for the Student Attendance System, built entirely using Python's standard library (no external dependencies) to meet project constraints.

## 📂 Database Architecture
The system uses a relational flat-file structure stored in the `/database` directory.
- `students.txt`: Registry of all students (`StudentID, Name`). Features auto-incrementing IDs.
- `users.txt`: Secure login credentials (`Username, Password_Hash, Role`). Passwords are encrypted using SHA-256.
- `courses.txt`: Available subjects (`CourseID, CourseName`).
- `teachers.txt`: Registry of faculty (`TeacherID, Name`).
- `enrollments.txt`: Bridge table connecting classes (`CourseID, TeacherID, StudentID`).
- `attendance.txt`: The transaction log (`Date, CourseID, StudentID, Status`).

## 🛠️ Key Features (Developer A)
1. **Automated Registration**: Registers a student and automatically provisions a secure user login in one action.
2. **Relational Class Filtering**: Ensures teachers only mark attendance for students actively enrolled in their specific courses.
3. **Data Validation**: Rejects invalid inputs (e.g., trying to mark attendance with a status other than 'P' or 'A').
4. **Data Standardization**: Robust string parsing using `.strip()` to prevent accidental whitespace from causing database search errors.

## 🚀 API Guide for UI Developers (Paulo & Indah)

### For Authentication & Setup
* `setup_database()`: Run once at app launch to verify file integrity.
* `verify_login(username, password, role)`: Returns `True` if credentials match.

### For Student UI
* `registration_student(name)`: Pass the student's name. It returns a success tuple containing the new auto-generated ID.

### For Teacher UI
* `get_all_courses()`: Returns a list of subjects to populate dropdowns.
* `get_students_for_class(course_id, teacher_id)`: Returns only the relevant students for the marking screen.
* `save_attendance(course_id, student_id, status)`: Saves 'P' or 'A' to the main ledger.

### For Reporting UI
* `get_attendance_records(student_id=None, course_id=None, date=None)`: Returns filtered records based on the parameters provided.

## 🧪 Unit Testing
To verify system integrity, run the separated test suite:
`python test_database.py`
This will automatically simulate registration, login validation, relational filtering, and edge-case data rejection.